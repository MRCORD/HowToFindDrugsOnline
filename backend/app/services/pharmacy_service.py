import logging
from typing import Optional, Dict
from datetime import datetime
from threading import Lock
from bson import ObjectId
from app.models.pharmacy import PharmacySearchRequest, PharmacyResponse, PharmacyUpdateResult, PharmacyUpdateStatus
from app.models.mongo import MongoQuery
from app.services.mongo_service import MongoService
from app.tasks.scrapers.pharmacy_scraper import scraper

class PharmacyService:
    # Static class variables for status tracking
    _update_status = PharmacyUpdateStatus()
    _status_lock = Lock()

    def __init__(self, db):
        self.db = db
        self.mongo_service = MongoService(db)
        self.logger = logging.getLogger(__name__)

    def get_raw_pharmacies(self, search_request: PharmacySearchRequest) -> Optional[PharmacyResponse]:
        try:
            return scraper.search_pharmacies(search_request)
        except Exception as e:
            self.logger.error(f"Error fetching raw pharmacy data: {str(e)}")
            return None

    @classmethod
    def get_update_status(cls) -> PharmacyUpdateStatus:
        with cls._status_lock:
            return cls._update_status

    def start_medicine_pharmacy_ids_update(self, background_tasks) -> str:
        """Start the update process in background"""
        with self.__class__._status_lock:
            if self.__class__._update_status.status == "running":
                return "Update already in progress"
            
            # Initialize status before starting background task
            self.__class__._update_status = PharmacyUpdateStatus(
                status="running",
                start_time=datetime.utcnow(),
                current_progress={
                    "processed": 0,
                    "total": 0
                }
            )

        # Add the update task to background tasks
        background_tasks.add_task(self._update_medicine_pharmacy_ids)
        return "Update process started"

    def _update_medicine_pharmacy_ids(self):
        try:
            # 1. First verify how many need updates in MEDICINES collection
            count_query = MongoQuery(
                db="health",
                collection="medicines",  # Changed from drugs to medicines
                aggregation=[
                    {
                        "$match": {
                            "comercio.pharmacyId": None
                        }
                    },
                    {
                        "$count": "total_null"
                    }
                ]
            )
            
            count_result = self.mongo_service.consult_mongo(count_query)
            initial_total = count_result.documents[0]["total_null"] if count_result.documents else 0
            self.logger.info(f"Initial documents needing update: {initial_total}")

            # 2. Get unique codEstabs from MEDICINES collection
            codestabs_query = MongoQuery(
                db="health",
                collection="medicines",  # Changed from drugs to medicines
                aggregation=[
                    {
                        "$match": {
                            "comercio.pharmacyId": None
                        }
                    },
                    {
                        "$group": {
                            "_id": "$comercio.codEstab",
                            "count": {"$sum": 1}
                        }
                    }
                ]
            )
            
            codestab_results = self.mongo_service.consult_mongo(codestabs_query)
            unique_codestabs = [doc["_id"] for doc in codestab_results.documents]

            self.logger.info(f"Found {len(unique_codestabs)} unique codEstabs")

            # 3. Get pharmacy mappings
            pharmacy_query = MongoQuery(
                db="health",
                collection="pharmacies",
                query={"codEstab": {"$in": unique_codestabs}},
                projection={"_id": 1, "codEstab": 1}
            )
            
            pharmacy_results = self.mongo_service.consult_mongo(pharmacy_query)
            
            pharmacy_mapping = {
                doc["codEstab"]: doc["_id"] 
                for doc in pharmacy_results.documents
            }

            self.logger.info(f"Found {len(pharmacy_mapping)} matching pharmacies")

            # 4. Batch updates on MEDICINES collection
            updated_total = 0
            processed = 0
            not_found_codestabs = []

            for codEstab in unique_codestabs:
                pharmacy_id = pharmacy_mapping.get(codEstab)
                
                if not pharmacy_id:
                    not_found_codestabs.append(codEstab)
                    self.logger.warning(f"No pharmacy found for codEstab: {codEstab}")
                else:
                    update_query = MongoQuery(
                        db="health",
                        collection="medicines",  # Changed from drugs to medicines
                        filter={
                            "comercio.codEstab": codEstab,
                            "comercio.pharmacyId": None
                        },
                        update={
                            "$set": {"comercio.pharmacyId": ObjectId(pharmacy_id)}
                        }
                    )

                    result = self.mongo_service.update_many(update_query)
                    modified_count = result.modified_count if result else 0
                    updated_total += modified_count
                    self.logger.info(f"Updated {modified_count} medicines for pharmacy {codEstab}")

                processed += 1
                with self.__class__._status_lock:
                    self.__class__._update_status.current_progress["processed"] = processed

            # 5. Final verification in MEDICINES collection
            final_count_result = self.mongo_service.consult_mongo(count_query)
            remaining = final_count_result.documents[0]["total_null"] if final_count_result.documents else 0
            
            self.logger.info(f"Update summary:")
            self.logger.info(f"Initial documents needing update: {initial_total}")
            self.logger.info(f"Documents updated: {updated_total}")
            self.logger.info(f"Documents still needing update: {remaining}")

            result = PharmacyUpdateResult(
                total_unique_codestabs=len(unique_codestabs),
                pharmacies_found=len(pharmacy_mapping),
                medicines_updated=updated_total,
                pharmacies_not_found=len(not_found_codestabs),
                not_found_codestabs=not_found_codestabs
            )

            with self.__class__._status_lock:
                self.__class__._update_status.status = "completed"
                self.__class__._update_status.end_time = datetime.utcnow()
                self.__class__._update_status.result = result
                self.logger.info(f"Update completed: {result}")

        except Exception as e:
            self.logger.error(f"Error updating pharmacy IDs: {str(e)}")
            with self.__class__._status_lock:
                self.__class__._update_status.status = "failed"
                self.__class__._update_status.end_time = datetime.utcnow()
                self.__class__._update_status.error = str(e)
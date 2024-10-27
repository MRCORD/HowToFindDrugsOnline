import logging
import time
from typing import Dict, Any, Optional, List, Set
from datetime import datetime
from bson import ObjectId
from app.models.mongo import MongoQuery
from app.services.mongo_service import MongoService
from app.tasks.scrapers.medicine_scraper import scraper, RateLimitException, ForbiddenException

class MedicineService:
    def __init__(self, db):
        self.db = db
        self.mongo_service = MongoService(db)
        self.logger = logging.getLogger(__name__)
        self.delay = 1
        self.max_retries = 8

    def search_medicines(self, product_data: Dict[str, Any], region_data: Dict[str, Any], exact_search: bool = False) -> Optional[Dict[str, Any]]:
        try:
            # Clean region data - allow None for codigoUbigeo
            clean_region_data = {
                "codigoDepartamento": region_data.get("codigoDepartamento"),
                "codigoProvincia": region_data.get("codigoProvincia"),
                "codigoUbigeo": region_data.get("codigoUbigeo") if region_data.get("codigoUbigeo") else None
            }
            
            # Clean product data - preserve empty strings
            clean_product_data = {
                "codigoProducto": product_data.get("codigoProducto"),
                "codGrupoFF": product_data.get("codGrupoFF"),
                "concent": product_data.get("concent", ""),  # Keep empty string
                "nombreProducto": product_data.get("nombreProducto") if exact_search else None  # None if not exact search
            }

            base_delay = 2
            max_delay = 30  # Reduced max delay
            
            # Single attempt for normal response
            self.logger.info(f"Searching with parameters: {clean_product_data}")
            time.sleep(base_delay)
            
            try:
                result = scraper.search_medicines(clean_product_data, clean_region_data, exact_search)
                if result and result.get('data'):
                    return result
                return None
                    
            except (RateLimitException, ForbiddenException) as e:
                # Only retry for rate limits
                self.logger.warning(f"Rate limit hit. Will retry with backoff.")
                for attempt in range(1, self.max_retries):
                    current_delay = min(base_delay * (2 ** attempt), max_delay)
                    self.logger.info(f"Waiting {current_delay} seconds before retry {attempt + 1}")
                    time.sleep(current_delay)
                    
                    try:
                        result = scraper.search_medicines(clean_product_data, clean_region_data, exact_search)
                        if result and result.get('data'):
                            return result
                    except (RateLimitException, ForbiddenException):
                        continue
                        
                return None
                    
        except Exception as e:
            self.logger.error(f"Error in search_medicines: {str(e)}")
            raise

    def process_document(self, document_id: str, region_data: Dict[str, str], limit: Optional[int] = None) -> Dict[str, Any]:
        try:
            query = MongoQuery(
                db="health",
                collection="searchterms",
                query={"_id": ObjectId(document_id)},
                limit=1
            )
            result = self.mongo_service.consult_mongo(query)
            
            if not result.documents:
                raise ValueError(f"Document with ID {document_id} not found")
            
            document = result.documents[0]
            concentrations = self._get_unique_concentrations(document)
            self.logger.info(f"Found {len(concentrations)} unique concentrations: {concentrations}")
            
            if limit:
                concentrations = list(concentrations)[:limit]
            
            stats = {
                "total_concentrations": len(concentrations),
                "processed": 0,
                "success": 0,
                "failed": 0,
                "transformed_data": [],
                "is_success": False  # New flag to track if any data was found
            }
            
            grupo = document.get("grupo")
            codGrupoFF = document.get("codGrupoFF")
            
            # Clean region data once
            clean_region_data = {
                k: v if v and str(v).strip() else None 
                for k, v in region_data.items()
            }
            
            self.logger.info(f"Using cleaned region data: {clean_region_data}")
            
            time.sleep(5)
            
            if not concentrations:
                self.logger.info("No concentrations found, searching by product name")
                for product in document.get("products", []):
                    try:
                        product_data = {
                            "codigoProducto": grupo,
                            "codGrupoFF": codGrupoFF,
                            "concent": "",
                            "nombreProducto": product.get("nombreProducto", "")
                        }
                        
                        self.logger.info(f"Searching with product parameters: {product_data}")
                        
                        raw_results = self.search_medicines(
                            product_data=product_data,
                            region_data=clean_region_data,
                            exact_search=True
                        )
                        
                        if raw_results and raw_results.get("data"):
                            transformed_data = [
                                self._transform_raw_data(raw_result) 
                                for raw_result in raw_results["data"]
                            ]
                            stats["transformed_data"].extend(transformed_data)
                            stats["success"] += 1
                            stats["is_success"] = True
                            self.logger.info(f"Found {len(transformed_data)} results for product {product.get('nombreProducto', '')}")
                        else:
                            self.logger.warning(f"No results found for product {product.get('nombreProducto', '')} with params: {product_data}")
                            stats["failed"] += 1
                        
                        time.sleep(3)
                        
                    except RateLimitException:
                        stats["failed"] += 1
                        raise
                        
                    except Exception as e:
                        self.logger.error(f"Error processing product {product.get('nombreProducto', '')}: {str(e)}")
                        stats["failed"] += 1
                    
                    stats["processed"] += 1
            else:
                for concent in concentrations:
                    try:
                        product_data = {
                            "codigoProducto": grupo,
                            "codGrupoFF": codGrupoFF,
                            "concent": concent,
                            "nombreProducto": ""
                        }
                        
                        self.logger.info(f"Searching with parameters: {product_data}")
                        
                        raw_results = self.search_medicines(
                            product_data=product_data,
                            region_data=clean_region_data,
                            exact_search=False
                        )
                        
                        if raw_results and raw_results.get("data"):
                            transformed_data = [
                                self._transform_raw_data(raw_result) 
                                for raw_result in raw_results["data"]
                            ]
                            stats["transformed_data"].extend(transformed_data)
                            stats["success"] += 1
                            stats["is_success"] = True
                            self.logger.info(f"Found {len(transformed_data)} results for concentration {concent}")
                        else:
                            self.logger.warning(f"No results found for concentration {concent} with params: {product_data}")
                            stats["failed"] += 1
                        
                        time.sleep(3)
                        
                    except RateLimitException:
                        stats["failed"] += 1
                        raise
                        
                    except Exception as e:
                        self.logger.error(f"Error processing concentration {concent}: {str(e)}")
                        stats["failed"] += 1
                    
                    stats["processed"] += 1
            
            if not stats["is_success"]:
                self.logger.warning(f"No data transformed for document {document_id}")
                raise ValueError(f"No data found for document {document_id}")
                
            return stats
            
        except Exception as e:
            self.logger.error(f"Error in process_document: {str(e)}")
            raise
    
    def _get_unique_concentrations(self, document: Dict[str, Any]) -> Set[str]:
        concentrations = set()
        for product in document.get("products", []):
            for variation in product.get("variations", []):
                if variation.get("concent"):
                    concentrations.add(variation["concent"])
        return concentrations

    def _transform_raw_data(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        try:
            fecha = datetime.strptime(raw.get("fecha", ""), "%d/%m/%Y %I:%M:%S %p")
            precios = {
                "precio1": raw.get("precio1"),
                "precio2": raw.get("precio2"),
                "precio3": raw.get("precio3")
            }
            
            return {
                "producto": {
                    "nombreProducto": raw.get("nombreProducto", ""),
                    "nombreSustancia": raw.get("nombreSustancia", ""),
                    "precios": precios,
                    "codProdE": raw.get("codProdE"),
                    "codGrupoFF": raw.get("codGrupoFF", ""),
                    "grupo": raw.get("grupo", ""),
                    "catCodigo": raw.get("catCodigo", ""),
                    "concent": raw.get("concent", ""),
                    "nombreFormaFarmaceutica": raw.get("nombreFormaFarmaceutica", ""),
                    "nomGrupoFF": raw.get("nomGrupoFF", ""),
                    "fracciones": raw.get("fracciones"),
                    "totalPA": raw.get("totalPA", ""),
                    "presentacion": raw.get("presentacion", None),
                    "registroSanitario": raw.get("registroSanitario", None),
                    "fabricante": {
                        "nombreLaboratorio": raw.get("nombreLaboratorio", ""),
                        "nombreTitular": raw.get("nombreTitular", "")
                    }
                },
                "comercio": {
                    "codEstab": raw.get("codEstab", ""),
                    "pharmacyId": None,
                    "setcodigo": raw.get("setcodigo", ""),
                    "nombreComercial": raw.get("nombreComercial", ""),
                    "locacion": {
                        "direccion": raw.get("direccion", None),
                        "distrito": raw.get("distrito", None)
                    }
                },
                "fecha": fecha.isoformat(),
                "historialPrecios": [{
                    "precios": precios,
                    "fecha": fecha.isoformat()
                }]
            }
        except Exception as e:
            self.logger.error(f"Error transforming raw data: {str(e)}")
            self.logger.error(f"Raw data: {raw}")
            raise

    def _get_or_create_processing_run(self, run_id: str, region_data: Dict[str, str]) -> Dict[str, Any]:
        query = MongoQuery(
            db="health",
            collection="processing_runs",
            query={"run_id": run_id}
        )
        result = self.mongo_service.consult_mongo(query)
        
        if result.documents:
            return result.documents[0]
        
        new_run = {
            "run_id": run_id,
            "status": "active",
            "start_time": datetime.utcnow(),
            "region_data": region_data,
            "processed_ids": [],
            "failed_ids": [],
            "total_stats": {
                "total_documents": 0,
                "processed": 0,
                "successful": 0,
                "failed": 0,
                "skipped": 0,
                "storage": {
                    "inserted": 0,
                    "updated": 0,
                    "unchanged": 0,
                    "failed": 0
                }
            }
        }
        
        self.mongo_service.insert_one({
            "db": "health",
            "collection": "processing_runs",
            "data": new_run
        })
        
        return new_run

    def _update_processing_run(self, run: Dict[str, Any]):
        """Update the processing run document excluding the _id field"""
        update_data = run.copy()
        update_data.pop('_id', None)
        
        update_query = MongoQuery(
            db="health",
            collection="processing_runs",
            filter={"run_id": run["run_id"]},
            update={"$set": update_data}
        )
        self.mongo_service.update_mongo(update_query)

    def get_processing_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        query = MongoQuery(
            db="health",
            collection="processing_runs",
            query={"run_id": run_id}
        )
        result = self.mongo_service.consult_mongo(query)
        return result.documents[0] if result.documents else None

    def process_all_documents(self, region_data: Dict[str, str], run_id: Optional[str] = None, batch_size: int = 100) -> Dict[str, Any]:
        try:
            if not run_id:
                run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
                
            processing_run = self._get_or_create_processing_run(run_id, region_data)
            
            unprocessed_docs = self._get_unprocessed_documents(processing_run)
            total_docs = len(unprocessed_docs)
            
            self.logger.info(f"Starting to process {total_docs} searchterm documents for run {run_id}")
            
            if processing_run["total_stats"]["total_documents"] == 0:
                processing_run["total_stats"]["total_documents"] = total_docs
            
            all_transformed_data = []  # Collect all transformed data
            current_batch_processed = []
            current_batch_failed = []
            
            # Process searchterm documents in batches
            for i in range(0, total_docs, batch_size):
                batch = unprocessed_docs[i:i + batch_size]
                self.logger.info(f"Processing batch {i//batch_size + 1} of {(total_docs + batch_size - 1)//batch_size}")
                
                for doc in batch:
                    doc_id = str(doc["_id"])
                    
                    if doc_id in processing_run["processed_ids"]:
                        continue
                    
                    try:
                        result = self.process_document(doc_id, region_data)
                        transformed_count = len(result["transformed_data"])
                        
                        if transformed_count > 0:
                            self.logger.info(f"Document {doc_id}: transformed {transformed_count} records from {result['total_concentrations']} concentrations")
                            all_transformed_data.extend(result["transformed_data"])
                            current_batch_processed.append(doc_id)

                            # Insert when we reach a good batch size
                            if len(all_transformed_data) >= 1000:
                                self.logger.info(f"INSERTING BATCH OF {len(all_transformed_data)} RECORDS TO MONGODB")
                                self.mongo_service.insert_many({
                                    "db": "health",
                                    "collection": "medicines",
                                    "data": all_transformed_data
                                })
                                self.logger.info(f"SUCCESSFULLY INSERTED {len(all_transformed_data)} RECORDS")
                                all_transformed_data = []  # Clear after successful insert
                                
                                # Update successful processed IDs
                                processing_run["processed_ids"].extend(current_batch_processed)
                                processing_run["total_stats"]["successful"] += len(current_batch_processed)
                                current_batch_processed = []
                        else:
                            self.logger.warning(f"Document {doc_id}: No data transformed from {result['total_concentrations']} concentrations")
                            current_batch_failed.append(doc_id)
                            
                    except Exception as e:
                        self.logger.error(f"Error processing document {doc_id}: {str(e)}")
                        current_batch_failed.append(doc_id)
                    
                    processing_run["total_stats"]["processed"] += 1
                    self._update_processing_run(processing_run)
                
                # Insert any remaining data
                if all_transformed_data:
                    self.logger.info(f"INSERTING REMAINING {len(all_transformed_data)} RECORDS TO MONGODB")
                    self.mongo_service.insert_many({
                        "db": "health",
                        "collection": "medicines",
                        "data": all_transformed_data
                    })
                    self.logger.info(f"SUCCESSFULLY INSERTED REMAINING {len(all_transformed_data)} RECORDS")
                    
                    processing_run["processed_ids"].extend(current_batch_processed)
                    processing_run["total_stats"]["successful"] += len(current_batch_processed)
                    all_transformed_data = []
                    current_batch_processed = []
                
                # Update failed IDs
                if current_batch_failed:
                    processing_run["failed_ids"].extend(current_batch_failed)
                    processing_run["total_stats"]["failed"] += len(current_batch_failed)
                    current_batch_failed = []
                
                self._update_processing_run(processing_run)
                
                self.logger.info(
                    f"Batch complete. Total documents processed successfully: {len(processing_run['processed_ids'])}, "
                    f"Failed: {len(processing_run['failed_ids'])}"
                )
            
            processing_run["status"] = "completed"
            processing_run["end_time"] = datetime.utcnow()
            self._update_processing_run(processing_run)
            
            return processing_run
            
        except Exception as e:
            self.logger.error(f"Error in process_all_documents: {str(e)}")
            if 'processing_run' in locals():
                processing_run["status"] = "failed"
                processing_run["end_time"] = datetime.utcnow()
                self._update_processing_run(processing_run)
            raise

    def _get_unprocessed_documents(self, processing_run: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get documents that come after the last failed document"""
        if processing_run["failed_ids"]:
            last_id = processing_run["failed_ids"][-1]
            query = MongoQuery(
                db="health",
                collection="searchterms",
                query={"_id": {"$gt": ObjectId(last_id)}},
                sort=[("_id", 1)]
            )
            self.logger.info(f"Continuing from document after: {last_id}")
        else:
            query = MongoQuery(
                db="health",
                collection="searchterms",
                query={},
                sort=[("_id", 1)]
            )
            self.logger.info("Starting from beginning")
        
        result = self.mongo_service.consult_mongo(query)
        return result.documents
    
    def retry_failed_documents(self, original_run_id: str, region_data: Optional[Dict[str, str]] = None, batch_size: int = 100) -> Dict[str, Any]:
        """Retry processing failed documents from a previous run"""
        try:
            # Get the original run
            query = MongoQuery(
                db="health",
                collection="processing_runs",
                query={"run_id": original_run_id}
            )
            result = self.mongo_service.consult_mongo(query)
            
            if not result.documents:
                raise ValueError(f"No processing run found with ID {original_run_id}")
                    
            original_run = result.documents[0]
            failed_ids = original_run.get("failed_ids", [])
            
            if not failed_ids:
                return {
                    "message": "No failed documents to retry",
                    "original_run_id": original_run_id,
                    "retry_run_id": None
                }
                    
            # Create new run for retry attempt
            base_run_id = original_run_id.replace("retry_", "") if original_run_id.startswith("retry_") else original_run_id
            retry_run_id = f"retry_{base_run_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
            
            region_data = region_data or original_run.get("region_data", {})
            if "codigoUbigeo" in region_data and not region_data["codigoUbigeo"]:
                region_data["codigoUbigeo"] = None
                    
            retry_run = {
                "run_id": retry_run_id,
                "original_run_id": original_run_id,
                "status": "active",
                "start_time": datetime.utcnow(),
                "region_data": region_data,
                "processed_ids": [],
                "failed_ids": [],
                "total_stats": {
                    "total_documents": len(failed_ids),
                    "processed": 0,
                    "successful": 0,
                    "failed": 0,
                    "skipped": 0
                }
            }
            
            insert_result = self.mongo_service.insert_one({
                "db": "health",
                "collection": "processing_runs",
                "data": retry_run
            })
            retry_run["_id"] = str(insert_result.inserted_id)
            
            # Process the documents
            all_transformed_data = []
            current_batch = []  # Track documents in current batch
            
            for doc_id in failed_ids:
                try:
                    self.logger.info(f"Processing document {doc_id}")
                    result = self.process_document(str(doc_id), region_data)
                    transformed_count = len(result.get("transformed_data", []))
                    
                    if transformed_count > 0:
                        self.logger.info(f"Successfully transformed {transformed_count} records for document {doc_id}")
                        all_transformed_data.extend(result["transformed_data"])
                        current_batch.append(doc_id)
                        retry_run["processed_ids"].append(str(doc_id))
                        retry_run["total_stats"]["successful"] += 1
                        
                        # Insert if batch threshold reached
                        if len(all_transformed_data) >= 1000:
                            try:
                                self.mongo_service.insert_many({
                                    "db": "health",
                                    "collection": "medicines",
                                    "data": all_transformed_data
                                })
                                self.logger.info(f"Successfully inserted batch of {len(all_transformed_data)} records")
                                all_transformed_data = []
                                current_batch = []
                            except Exception as e:
                                self.logger.error(f"Error inserting batch: {str(e)}")
                                retry_run["total_stats"]["failed"] += len(current_batch)
                                retry_run["failed_ids"].extend(current_batch)
                                all_transformed_data = []
                                current_batch = []
                    else:
                        self.logger.warning(f"No data transformed for document {doc_id}")
                        retry_run["failed_ids"].append(str(doc_id))
                        retry_run["total_stats"]["failed"] += 1
                    
                except ValueError as ve:
                    self.logger.warning(f"No data found for document {doc_id}: {str(ve)}")
                    retry_run["failed_ids"].append(str(doc_id))
                    retry_run["total_stats"]["failed"] += 1
                except Exception as e:
                    self.logger.error(f"Error processing document {doc_id}: {str(e)}")
                    retry_run["failed_ids"].append(str(doc_id))
                    retry_run["total_stats"]["failed"] += 1
                
                retry_run["total_stats"]["processed"] += 1
                self._update_processing_run(retry_run)
            
            # Insert any remaining data
            if all_transformed_data:
                try:
                    self.mongo_service.insert_many({
                        "db": "health",
                        "collection": "medicines",
                        "data": all_transformed_data
                    })
                    self.logger.info(f"Successfully inserted final batch of {len(all_transformed_data)} records")
                except Exception as e:
                    self.logger.error(f"Error inserting final batch: {str(e)}")
                    retry_run["total_stats"]["failed"] += len(current_batch)
                    retry_run["failed_ids"].extend(current_batch)
                    # Adjust successful count for failed insertion
                    retry_run["total_stats"]["successful"] -= len(current_batch)
                    retry_run["processed_ids"] = [id for id in retry_run["processed_ids"] if id not in current_batch]
            
            # Complete the run
            retry_run["status"] = "completed"
            retry_run["end_time"] = datetime.utcnow()
            self._update_processing_run(retry_run)
            
            return retry_run
                
        except Exception as e:
            self.logger.error(f"Error in retry_failed_documents: {str(e)}")
            if 'retry_run' in locals():
                retry_run["status"] = "failed"
                retry_run["end_time"] = datetime.utcnow()
                self._update_processing_run(retry_run)
            raise
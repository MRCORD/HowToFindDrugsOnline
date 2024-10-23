import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime
from app.models.mongo import MongoQuery
from app.services.mongo_service import MongoService
from app.tasks.scrapers.medicine_scraper import scraper, RateLimitException, ForbiddenException

class MedicineService:
    def __init__(self, db):
        self.db = db
        self.mongo_service = MongoService(db)
        self.logger = logging.getLogger(__name__)
        self.delay = 1  # Start with a 1-second delay
        self.max_retries = 8

    def search_medicines(self, product_data: Dict[str, Any], region_data: Dict[str, Any], exact_search: bool = False) -> Optional[Dict[str, Any]]:
        for attempt in range(self.max_retries):
            try:
                time.sleep(self.delay)
                result = scraper.search_medicines(product_data, region_data, exact_search)
                self.delay = 1  # Reset delay on success
                
                # Store the search result in MongoDB
                if result:
                    self._store_search_result(result, product_data, region_data)
                
                return result

            except RateLimitException:
                self.logger.warning(f"Rate limit hit. Retrying in {self.delay} seconds.")
                time.sleep(self.delay)
                self.delay *= 2  # Exponential backoff
            
            except ForbiddenException:
                self.logger.error(f"Access forbidden. Waiting for {self.delay} seconds before retry.")
                time.sleep(self.delay)
                self.delay *= 2  # Exponential backoff
            
            except Exception as e:
                self.logger.error(f"Error searching medicines: {str(e)}")
                return None
        
        self.logger.error("Max retries reached")
        return None

    def _store_search_result(self, result: Dict[str, Any], product_data: Dict[str, Any], region_data: Dict[str, Any]):
        try:
            document = {
                "search_data": {
                    "product": product_data,
                    "region": region_data
                },
                "result": result,
                "timestamp": datetime.utcnow()
            }
            
            self.mongo_service.insert_one({
                "db": "health",
                "collection": "medicine_searches",
                "data": document
            })
            
        except Exception as e:
            self.logger.error(f"Error storing search result: {str(e)}")

    def get_recent_searches(self, limit: int = 10) -> list:
        query = MongoQuery(
            db="health",
            collection="medicine_searches",
            query={},
            sort=[("timestamp", -1)],
            limit=limit
        )
        result = self.mongo_service.consult_mongo(query)
        return result.documents
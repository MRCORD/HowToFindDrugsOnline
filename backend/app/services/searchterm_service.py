import logging
import time
from app.models.searchterm import RawSearchTermData
from app.models.mongo import MongoQuery
from app.services.mongo_service import MongoService
from typing import List, Dict, Optional
from datetime import datetime
from app.tasks.scrapers.searchterm_scraper import scraper, RateLimitException
from bson import ObjectId

class SearchTermService:
    def __init__(self, db):
        self.db = db
        self.mongo_service = MongoService(db)
        self.logger = logging.getLogger(__name__)
        self.delay = 1  # Start with a 1-second delay
        self.max_retries = 5

    def get_catalog_items(self, limit: Optional[int] = None) -> List[Dict]:
        query = MongoQuery(
            db="health",
            collection="catalog",
            query={},
            projection={"name": 1},
            limit=limit if limit is not None else 0
        )
        result = self.mongo_service.consult_mongo(query)
        return result.documents

    def get_raw_search_terms(self, search_term: str) -> Optional[List[RawSearchTermData]]:
        for attempt in range(self.max_retries):
            try:
                time.sleep(self.delay)
                result = scraper.fetch_search_terms(search_term)
                self.delay = 1  # Reset delay on success
                return result
            except RateLimitException:
                self.logger.warning(f"Rate limit hit for {search_term}. Retrying in {self.delay} seconds.")
                time.sleep(self.delay)
                self.delay *= 2  # Exponential backoff
            except Exception as e:
                self.logger.error(f"Error fetching search terms for {search_term}: {str(e)}")
                return None
        
        self.logger.error(f"Max retries reached for {search_term}")
        return None
    
    def process_catalog_items(self, limit: Optional[int] = None):
        catalog_items = self.get_catalog_items(limit)
        self.logger.info(f"Processing {len(catalog_items)} catalog items")
        for item in catalog_items:
            self.logger.info(f"Processing search term: {item['name']}")
            self.process_search_term(item['name'])
            time.sleep(1)  # Add a small delay between items to avoid overwhelming the API
        self.logger.info("Catalog processing completed")

    def process_search_term(self, search_term: str):
        raw_data = self.get_raw_search_terms(search_term)
        if not raw_data:
            self.logger.warning(f"No results found for search term: {search_term}")
            return

        self.logger.info(f"Found {len(raw_data)} results for search term: {search_term}")
        for item in raw_data:
            self.update_or_create_document(item, search_term)

    def update_or_create_document(self, item: RawSearchTermData, search_term: str):
        group_doc = self.find_or_create_group_document(item.grupo, item.codGrupoFF)
        if group_doc:
            self.update_product_in_group(group_doc, item, search_term)
        else:
            self.logger.error(f"Failed to find or create group document for grupo {item.grupo} and codGrupoFF {item.codGrupoFF}")

    def find_or_create_group_document(self, grupo: int, codGrupoFF: str) -> Optional[Dict]:
        query = MongoQuery(
            db="health",
            collection="searchterms",
            query={
                "grupo": grupo,
                "codGrupoFF": codGrupoFF
            },
            limit=1
        )
        result = self.mongo_service.consult_mongo(query)
        
        if result.documents:
            self.logger.info(f"Found existing group document for grupo {grupo} and codGrupoFF {codGrupoFF}")
            return result.documents[0]
        else:
            self.logger.info(f"Creating new group document for grupo {grupo} and codGrupoFF {codGrupoFF}")
            new_doc = {
                "grupo": grupo,
                "codGrupoFF": codGrupoFF,
                "products": [],
                "last_updated": datetime.utcnow()
            }
            try:
                insert_result = self.mongo_service.insert_one({
                    "db": "health",
                    "collection": "searchterms",
                    "data": new_doc
                })
                new_doc["_id"] = str(insert_result.inserted_id)
                return new_doc
            except Exception as e:
                self.logger.error(f"Error inserting new document: {str(e)}")
                return None

    def update_product_in_group(self, group_doc: Dict, item: RawSearchTermData, search_term: str):
        product = next((p for p in group_doc["products"] if p["nombreProducto"] == item.nombreProducto), None)
        
        if not product:
            self.logger.info(f"Adding new product {item.nombreProducto} to group")
            product = self.create_product(item, search_term)
            group_doc["products"].append(product)
        else:
            self.logger.info(f"Updating existing product {item.nombreProducto} in group")
            variation = next((v for v in product["variations"] if v["concent"] == item.concent and v["nombreFormaFarmaceutica"] == item.nombreFormaFarmaceutica), None)
            
            if not variation:
                product["variations"].append(self.create_variation(item, search_term))
            elif search_term not in variation["search_terms"]:
                variation["search_terms"].append(search_term)

        update_result = self.mongo_service.update_mongo(MongoQuery(
            db="health",
            collection="searchterms",
            filter={"_id": ObjectId(group_doc["_id"])},
            update={
                "$set": {
                    "products": group_doc["products"],
                    "last_updated": datetime.utcnow()
                }
            }
        ))
        self.logger.info(f"Update result: {update_result.modified_count} document(s) modified")

    def create_product(self, item: RawSearchTermData, search_term: str) -> Dict:
        return {
            "nombreProducto": item.nombreProducto,
            "variations": [self.create_variation(item, search_term)]
        }

    def create_variation(self, item: RawSearchTermData, search_term: str) -> Dict:
        return {
            "codigoProducto": item.codigoProducto,
            "concent": item.concent,
            "presentacion": item.presentacion,
            "fracciones": item.fracciones,
            "nombreFormaFarmaceutica": item.nombreFormaFarmaceutica,
            "nroRegistroSanitario": item.nroRegistroSanitario,
            "titular": item.titular,
            "search_terms": [search_term]
        }

    def get_search_terms_from_db(self, search_term: str = None) -> List[dict]:
        query = {}
        if search_term:
            query = {"products.variations.search_terms": search_term}
        
        mongo_query = MongoQuery(
            db="health",
            collection="searchterms",
            query=query,
            limit=0
        )
        result = self.mongo_service.consult_mongo(mongo_query)
        return result.documents
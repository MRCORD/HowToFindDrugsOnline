import logging
from app.models.generics import RawGenericData, GenericProduct, GenericVariation
from app.models.mongo import MongoQuery
from app.services.mongo_service import MongoService
from typing import List, Dict
from datetime import datetime
from app.tasks.scrapers.generics_scraper import scraper

class GenericsService:
    def __init__(self, db):
        self.db = db
        self.mongo_service = MongoService(db)
        self.logger = logging.getLogger(__name__)

    def get_raw_generics(self) -> List[RawGenericData]:
        return scraper.fetch_generics()

    def get_generics_from_db(self) -> List[dict]:
        query = MongoQuery(
            db="health",
            collection="generics",
            query={},
            limit=0
        )
        result = self.mongo_service.consult_mongo(query)
        return result.documents

    def update_generics(self, raw_data: List[RawGenericData]) -> Dict[str, int]:
        product_groups = {}
        for item in raw_data:
            if item.Nom_Prod not in product_groups:
                product_groups[item.Nom_Prod] = []
            product_groups[item.Nom_Prod].append(item)

        total = len(product_groups)
        updated = 0
        added = 0
        failed = 0

        for product_name, variations in product_groups.items():
            try:
                result = self._update_product(product_name, variations)
                if result == "updated":
                    updated += 1
                elif result == "added":
                    added += 1
            except Exception as e:
                self.logger.error(f"Failed to update product {product_name}: {str(e)}")
                failed += 1

        self.logger.info(f"Update completed. Total: {total}, Updated: {updated}, Added: {added}, Failed: {failed}")
        return {"total": total, "updated": updated, "added": added, "failed": failed}

    def _update_product(self, product_name: str, variations: List[dict]) -> str:
        existing_product = self.mongo_service.consult_mongo(MongoQuery(
            db="health",
            collection="generics",
            query={"name": product_name},
            limit=1
        )).documents

        if existing_product:
            existing_product_dict = dict(existing_product[0])
            updated_variations = self._merge_variations(existing_product_dict['variations'], variations)
            update_query = MongoQuery(
                db="health",
                collection="generics",
                filter={"name": product_name},
                update={"$set": {"variations": updated_variations}}
            )
            self.mongo_service.update_mongo(update_query)
            return "updated"
        else:
            self.mongo_service.insert_one({
                "db": "health",
                "collection": "generics",
                "data": {
                    "name": product_name,
                    "variations": [variation.dict() for variation in variations]
                }
            })
            return "added"

    def _merge_variations(self, existing_variations: List[dict], new_variations: List[RawGenericData]) -> List[dict]:
        merged = {var['Cod_Prod']: var for var in existing_variations}
        for new_var in new_variations:
            if new_var.Cod_Prod in merged:
                merged[new_var.Cod_Prod].update(new_var.dict())
                merged[new_var.Cod_Prod]['last_modified'] = datetime.utcnow()
            else:
                merged[new_var.Cod_Prod] = GenericVariation(**new_var.dict()).dict()
        return list(merged.values())

    def update_all_generics(self) -> Dict[str, int]:
        raw_generics = self.get_raw_generics()
        if not raw_generics:
            self.logger.error("Failed to fetch raw generics data")
            return {"total": 0, "updated": 0, "added": 0, "failed": 0}
        return self.update_generics(raw_generics)
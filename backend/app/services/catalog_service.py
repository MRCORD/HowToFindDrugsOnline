import logging
from app.models.catalog import RawCatalogData, CatalogProduct, CatalogVariation
from app.models.mongo import MongoQuery
from app.services.mongo_service import MongoService
from typing import List, Dict
from datetime import datetime
from app.tasks.scrapers.catalog_scraper import scraper

class CatalogService:
    def __init__(self, db):
        self.db = db
        self.mongo_service = MongoService(db)
        self.logger = logging.getLogger(__name__)

    def get_raw_catalog(self) -> List[RawCatalogData]:
        return scraper.fetch_catalog()

    def get_raw_excel(self):
        return scraper.fetch_raw_excel()

    def get_catalog_from_db(self) -> List[dict]:
        query = MongoQuery(
            db="health",
            collection="catalog",
            query={},
            limit=0
        )
        result = self.mongo_service.consult_mongo(query)
        return result.documents

    def update_catalog(self, raw_data: List[RawCatalogData]) -> Dict[str, int]:
        product_groups = {}
        for item in raw_data:
            if item.Nombre not in product_groups:
                product_groups[item.Nombre] = []
            product_groups[item.Nombre].append(item)

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

    def _update_product(self, product_name: str, variations: List[RawCatalogData]) -> str:
        existing_product = self.mongo_service.consult_mongo(MongoQuery(
            db="health",
            collection="catalog",
            query={"name": product_name},
            limit=1
        )).documents

        if existing_product:
            existing_product_dict = dict(existing_product[0])
            updated_variations = self._merge_variations(existing_product_dict['variations'], variations)
            update_query = MongoQuery(
                db="health",
                collection="catalog",
                filter={"name": product_name},
                update={
                    "$set": {
                        "variations": updated_variations,
                        "last_updated": datetime.utcnow()
                    }
                }
            )
            self.mongo_service.update_mongo(update_query)
            return "updated"
        else:
            new_product = CatalogProduct(
                name=product_name,
                variations=[self._create_variation(var) for var in variations],
                last_updated=datetime.utcnow()
            )
            self.mongo_service.insert_one({
                "db": "health",
                "collection": "catalog",
                "data": new_product.dict()
            })
            return "added"

    def _merge_variations(self, existing_variations: List[dict], new_variations: List[RawCatalogData]) -> List[dict]:
        merged = {var['Codigo']: var for var in existing_variations}
        for new_var in new_variations:
            if new_var.Codigo in merged:
                merged[new_var.Codigo].update(new_var.dict())
                merged[new_var.Codigo]['last_modified'] = datetime.utcnow()
            else:
                merged[new_var.Codigo] = self._create_variation(new_var).dict()
        return list(merged.values())

    def _create_variation(self, raw_data: RawCatalogData) -> CatalogVariation:
        return CatalogVariation(
            **raw_data.dict(),
            last_modified=datetime.utcnow()
        )

    def update_all_catalog(self) -> Dict[str, int]:
        raw_catalog = self.get_raw_catalog()
        if not raw_catalog:
            self.logger.error("Failed to fetch raw catalog data")
            return {"total": 0, "updated": 0, "added": 0, "failed": 0}
        return self.update_catalog(raw_catalog)
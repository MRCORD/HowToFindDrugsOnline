from app.core.database import db
from app.services.drugs_service import DrugsService
from app.services.generics_service import GenericsService
from app.services.mongo_service import MongoService
from app.services.catalog_service import CatalogService

def get_mongo_service():
    return MongoService(db)

def get_drugs_service():
    mongo_service = get_mongo_service()
    return DrugsService(mongo_service)

def get_generics_service():
    return GenericsService(db)

def get_catalog_service():
    return CatalogService(db)
from fastapi import APIRouter, Depends, HTTPException

from .models import *
from .utils import *

import logging

# Create an APIRouter instance
router = APIRouter()


#Logger
#====================================================================================================

# Create a logger for the views module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set the log level to INFO

# Create a file handler and set its log level
file_handler = logging.FileHandler('app.log')  # Create or append to the 'app.log' file
file_handler.setLevel(logging.INFO)

# Define a formatter for file output
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)
#====================================================================================================

@router.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome"}


@router.post("/v1/consult_mongo", tags=["MongoDB", "Production"])
def consult_mongo(request: MongoQuery):
    
    try:
        documents = consult_mongo_data(request)
        
        if documents is None:
            raise HTTPException(status_code=500, detail="Error retrieving MongoDB query")
        
        # Convert ObjectId to string to ensure JSON serialization compatibility
        documents = [convert_objectid(doc) for doc in documents]

        # Convert documents to a list of GenericDocument instances
        result = ResponseModel(documents=documents) #=[GenericDocument(data=doc) for doc in documents])

        logger.info(f"MongoDB query retrieved successfully with {len(result.documents)} documents")
        return result
    
    except HTTPException as e:
        logger.error(f"HTTPException: {str(e)}")
        raise e
    
    except Exception as e:
        logger.error(f"Error retrieving MongoDB query: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving MongoDB query")

@router.get("/v1/unique_drugs", tags=["queries", "Production"])
def get_unique_drugs():
    try:
        consult_body = {
            "db": "health",
            "collection": "drugs",
            "aggregation": [
                {"$group": {
                    "_id": {
                        "searchTerm": "$searchTerm",
                        "concent": "$producto.concent",
                        "nombreFormaFarmaceutica": "$producto.nombreFormaFarmaceutica"
                    }}},
                {"$sort": {
                    "_id.searchTerm": 1,
                    "_id.concent": 1,
                    "_id.nombreFormaFarmaceutica": 1
                }},
                {"$project": {
                    "_id": 0,
                    "searchTerm": "$_id.searchTerm",
                    "concent": "$_id.concent",
                    "nombreFormaFarmaceutica": "$_id.nombreFormaFarmaceutica"
                }}
            ]
        }
        documents = consult_mongo_data(MongoQuery(**consult_body))
        if documents is None:
            raise HTTPException(status_code=500, detail="Error retrieving unique drugs")
        return {"drugs": documents}
    except Exception as e:
        logger.error(f"Error retrieving unique drugs: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving unique drugs")
    

@router.get("/v1/unique_districts", tags=["queries", "Production"])
def get_unique_districts():
    try:
        consult_body = {
            "db": "peru",
            "collection": "districts",
            "aggregation": [
                {"$project": {"_id": 0, "descripcion": 1}},
                {"$sort": {"descripcion": 1}}
            ]
        }
        documents = consult_mongo_data(MongoQuery(**consult_body))
        if documents is None:
            raise HTTPException(status_code=500, detail="Error retrieving unique districts")
        return {"districts": documents}
    except Exception as e:
        logger.error(f"Error retrieving unique districts: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving unique districts")



@router.post("/v1/filtered_drugs", tags=["queries", "Production"])
def get_filtered_drugs(request: FilteredDrugRequest):
    try:
        consult_body = {
            "db": "health",
            "collection": "drugs",
            "aggregation": [
                {
                    '$match': {
                        "searchTerm": request.selected_drug,
                        "producto.concent": request.concent,
                        "producto.nombreFormaFarmaceutica": request.nombreFormaFarmaceutica,
                        "comercio.locacion.distrito": request.selected_distrito
                    }
                },
                {'$sort': {'producto.precios.precio2': 1}},
                {'$limit': 3},
                {'$lookup': {
                    'from': 'pharmacies',
                    'localField': 'comercio.pharmacyId',
                    'foreignField': '_id',
                    'as': 'pharmacyInfo'
                }},
                {'$project': {
                    '_id': 1,
                    'nombreProducto': '$producto.nombreProducto',
                    'concent': '$producto.concent',
                    'nombreFormaFarmaceutica': '$producto.nombreFormaFarmaceutica',
                    'precio2': '$producto.precios.precio2',
                    'nombreComercial': {'$arrayElemAt': ['$pharmacyInfo.nombreComercial', 0]},
                    'direccion': {'$arrayElemAt': ['$pharmacyInfo.locacion.direccion', 0]},
                    'googleMaps_search_url': {'$arrayElemAt': ['$pharmacyInfo.google_maps.googleMaps_search_url', 0]},
                    'googleMapsUri': {'$arrayElemAt': ['$pharmacyInfo.google_maps.googleMapsUri', 0]}
                }}
            ]
        }
        documents = consult_mongo_data(MongoQuery(**consult_body))
        if documents is None:
            raise HTTPException(status_code=500, detail="Error retrieving filtered drugs")
        
        return {"drugs": documents}
    except Exception as e:
        logger.error(f"Error retrieving filtered drugs: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving filtered drugs")

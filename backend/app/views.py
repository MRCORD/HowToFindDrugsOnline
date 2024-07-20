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


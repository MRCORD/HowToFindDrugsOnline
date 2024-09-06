import pandas as pd
import requests
import json
import time

from pymongo import MongoClient
from bson import ObjectId

from requests.exceptions import HTTPError, ConnectionError

import logging

from dotenv import load_dotenv
import os

load_dotenv()

#Logger
#====================================================================================================

# Create a logger for the utils module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set the log level to INFO

# Create a file handler and set its log level
file_handler = logging.FileHandler('utils.log')  # Create or append to the 'utils.log' file
file_handler.setLevel(logging.INFO)

# Define a formatter for file output
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)
#====================================================================================================


def consult_meds_digemid(product_data, region_data, max_retries=3):
    url = "https://ms-opm.minsa.gob.pe/msopmcovid/preciovista/ciudadano"
    
    headers = {
        "Origin": "https://opm-digemid.minsa.gob.pe",
        "Referer": "https://opm-digemid.minsa.gob.pe/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
    }
    
    payload = {
        "filtro": {
            "codigoProducto": product_data.codigoProducto,  
            "codigoDepartamento": region_data.codigoDepartamento,  
            "codigoProvincia": region_data.codigoProvincia,  
            "codigoUbigeo": region_data.codigoUbigeo,  
            "codTipoEstablecimiento": None,
            "catEstablecimiento": None,
            "codGrupoFF": product_data.codGrupoFF,  
            "concent": product_data.concent,  
            "tamanio": 100000,
            "pagina": 1,
            "nombreProducto": None
        }
    }
    
    try:
        retries = 0
        while retries < max_retries:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            if response.status_code == 200:
                logger.info("Request Meds DIGEMID was successful")
                return response.json()
            elif response.status_code in [429,500]:
                retries += 1
                wait_time = 2 ** retries  # Exponential backoff
                logger.warning(f"Request Meds DIGEMID failed with status code: {response.status_code}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logger.error(f"Request Meds DIGEMID failed with status code: {response.status_code}")
                logger.error(f"Request Meds DIGEMID failed after {max_retries} retries")
                return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request Meds DIGEMID failed with exception: {e}")
        return None
    

def consult_details_digemid(codEstablecimiento, codProducto, max_retries=3):
    url = "https://ms-opm.minsa.gob.pe/msopmcovid/precioproducto/obtener"

    headers = {
        "Origin": "https://opm-digemid.minsa.gob.pe",
        "Referer": "https://opm-digemid.minsa.gob.pe/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
    }
        
    payload = {
        "filtro": {
            "codEstablecimiento": codEstablecimiento,
            "codigoProducto": codProducto,
        }
    }
    
    try:
        retries = 0
        while retries < max_retries:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            if response.status_code == 200:
                logger.info("Request Details DIGEMID was successful")
                return response.json()
            elif response.status_code in [429,500]:
                retries += 1
                wait_time = 2 ** retries
            else:
                logger.error(f"Request Details DIGEMID failed with status code: {response.status_code}")
                logger.error(f"Request Details DIGEMID failed after {max_retries} retries")
                return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request Details DIGEMID failed with exception: {e}")
        return None

def convert_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {k: convert_objectid(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_objectid(v) for v in obj]
    else:
        return obj

def consult_mongo_data(query):
    try:
        connection_string = os.environ.get("MONGODB_CONNECTION_STRING")
        if not connection_string:
            logger.error("MongoDB connection string not found in environment variables")
            return None

        client = MongoClient(connection_string,
                             socketTimeoutMS=60000,
                             connectTimeoutMS=60000,
                             )
        db = client[query.db]
        collection = db[query.collection]
        logger.info("MongoDB connection was successful")

        # Ping the MongoDB server to check if it's available
        client.server_info()
        logger.info("MongoDB server is available")

        if query.aggregation:
            # Perform aggregation pipeline if aggregation is provided
            cursor = collection.aggregate(query.aggregation)
        else:
            # Perform find query with query and limit parameters
            cursor = collection.find(query.query).limit(query.limit or 0)

        # Fetch the documents from the cursor and convert ObjectId to string
        documents = [convert_objectid(doc) for doc in cursor]

        logger.info(f"MongoDB query length: {len(documents)}")
        return documents
    except Exception as e:
        logger.error(f"MongoDB query failed with exception: {e}")
        return None
    finally:
        client.close()
        
def medicineOption_concat(medicine_info):
    medicine_dropdown = f"{medicine_info['searchTerm']} {medicine_info['concent']} [{medicine_info['nombreFormaFarmaceutica']}]"
    return medicine_dropdown
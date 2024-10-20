import requests
import pandas as pd
import io
import logging
from datetime import datetime
from requests.exceptions import RequestException
from app.models.catalog import RawCatalogData

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CatalogScraper:
    def __init__(self):
        self.url = "https://ms-opm.minsa.gob.pe/msopmcovid/producto/catalogoproductos"
        self.session = requests.Session()
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://opm-digemid.minsa.gob.pe",
            "Referer": "https://opm-digemid.minsa.gob.pe/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0.1 Safari/605.1.15"
        }

    def get_token(self):
        # For now, we'll use a placeholder token
        return "PLACEHOLDER_TOKEN"

    def fetch_raw_excel(self):
        try:
            token = self.get_token()
            payload = {
                "filtro": {
                    "situacion": "ACT",
                    "tokenGoogle": token
                }
            }
            
            logger.info(f"Sending POST request to {self.url}")
            logger.debug(f"Headers: {self.headers}")
            logger.debug(f"Payload: {payload}")

            response = self.session.post(self.url, headers=self.headers, json=payload, stream=True)
            
            logger.info(f"Received response with status code: {response.status_code}")
            logger.debug(f"Response headers: {response.headers}")

            response.raise_for_status()

            content_type = response.headers.get('Content-Type', '')
            logger.info(f"Content-Type of response: {content_type}")

            return io.BytesIO(response.content)
        except RequestException as e:
            logger.error(f"Error fetching catalog data: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response content: {e.response.text}")
            return None

    def fetch_catalog(self):
        excel_content = self.fetch_raw_excel()
        if excel_content is None:
            return None
        
        try:
            df = pd.read_excel(excel_content, engine='openpyxl', header=None)
            logger.info(f"Successfully read Excel file. Shape: {df.shape}")

            update_date_str = df.iloc[5, 1]
            update_date = datetime.strptime(update_date_str, "%d/%m/%Y %I:%M:%S %p")
            logger.info(f"Catalog update date: {update_date}")

            data_df = df.iloc[6:]
            data_df.columns = data_df.iloc[0]
            data_df = data_df.iloc[1:].reset_index(drop=True)

            logger.debug(f"Columns after processing: {data_df.columns}")
            logger.debug(f"First few rows of data:\n{data_df.head().to_string()}")

            data = []
            for _, row in data_df.iterrows():
                data.append(RawCatalogData(
                    Codigo=str(row.get('Cod_Prod', '')),
                    Nombre=str(row.get('Nom_Prod', '')),
                    Concentracion=str(row.get('Concent', '')),
                    Forma_Farmaceutica=str(row.get('Nom_Form_Farm', '')),
                    Presentac=str(row.get('Presentac', '')),
                    Fraccion=str(row.get('Fracción', '')),
                    Registro_Sanitario=str(row.get('Num_RegSan', '')),
                    Nom_Titular=str(row.get('Nom_Titular', '')),
                    Laboratorio=str(row.get('Nom_Fabricante', '')),
                    Nom_IFA=str(row.get('Nom_IFA', '')),
                    Nom_Rubro=str(row.get('Nom_Rubro', '')),
                    Situacion=str(row.get('Situación', '')),
                    Fecha_Actualizacion=update_date
                ))
            
            logger.info(f"Processed {len(data)} rows of data")
            return data
        except Exception as e:
            logger.error(f"Error processing Excel data: {str(e)}")
            logger.debug(f"DataFrame head: {df.head()}")
            logger.debug(f"DataFrame columns: {df.columns}")
            return None

scraper = CatalogScraper()
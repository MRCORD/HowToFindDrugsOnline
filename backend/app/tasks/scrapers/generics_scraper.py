import requests
import pandas as pd
import io
from app.models.generics import RawGenericData

class GenericsScraper:
    def __init__(self):
        self.url = "http://observatorio.digemid.minsa.gob.pe/medicamentosesenciales/genericos.csv"

    def fetch_generics(self):
        try:
            headers = {
                "Origin": "https://opm-digemid.minsa.gob.pe",
                "Referer": "https://opm-digemid.minsa.gob.pe/",
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
            }

            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
            
            decoded_content = response.content.decode('utf-8')
            csv_content = io.StringIO(decoded_content)
            df = pd.read_csv(csv_content)
            
            generics = [RawGenericData(**row.to_dict()) for _, row in df.iterrows()]
            return generics
        except Exception as e:
            print(f"Error fetching generics data: {e}")
            return None

scraper = GenericsScraper()
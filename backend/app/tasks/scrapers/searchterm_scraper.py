import requests
import time
import random
from app.models.searchterm import RawSearchTermData

class RateLimitException(Exception):
    pass

class ForbiddenException(Exception):
    pass

class SearchTermsScraper:
    def __init__(self):
        self.url = "https://ms-opm.minsa.gob.pe/msopmcovid/producto/autocompleteciudadano"
        self.headers = {
            "Origin": "https://opm-digemid.minsa.gob.pe",
            "Referer": "https://opm-digemid.minsa.gob.pe/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }
        self.session = requests.Session()

    def fetch_search_terms(self, search_term):
        try:
            # Mimic human behavior by adding a random delay
            time.sleep(random.uniform(1, 3))

            payload = {
                "filtro": {
                    "nombreProducto": search_term,
                    "pagina": 1,
                    "tamanio": 100,
                }
            }

            response = self.session.post(self.url, headers=self.headers, json=payload)
            
            if response.status_code == 429:
                raise RateLimitException("Rate limit exceeded")
            elif response.status_code == 403:
                raise ForbiddenException("Access forbidden")
            
            response.raise_for_status()
            
            json_data = response.json()
            
            search_terms_data = []
            for item in json_data.get('data', []):
                search_terms_data.append(RawSearchTermData(
                    codigoProducto=item.get('codigoProducto'),
                    nombreProducto=item.get('nombreProducto'),
                    concent=item.get('concent'),
                    presentacion=item.get('presentacion'),
                    fracciones=item.get('fracciones'),
                    nombreFormaFarmaceutica=item.get('nombreFormaFarmaceutica'),
                    nroRegistroSanitario=item.get('nroRegistroSanitario'),
                    titular=item.get('titular'),
                    grupo=item.get('grupo'),
                    codGrupoFF=item.get('codGrupoFF')
                ))
            
            return search_terms_data
        except (RateLimitException, ForbiddenException):
            raise
        except Exception as e:
            print(f"Error fetching search terms data: {e}")
            raise

scraper = SearchTermsScraper()
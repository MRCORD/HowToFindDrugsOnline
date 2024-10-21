import requests
from app.models.searchterm import RawSearchTermData

class RateLimitException(Exception):
    pass

class SearchTermsScraper:
    def __init__(self):
        self.url = "https://ms-opm.minsa.gob.pe/msopmcovid/producto/autocompleteciudadano"
        self.headers = {
            "Origin": "https://opm-digemid.minsa.gob.pe",
            "Referer": "https://opm-digemid.minsa.gob.pe/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
            "Content-Type": "application/json"
        }

    def fetch_search_terms(self, search_term):
        try:
            payload = {
                "filtro": {
                    "nombreProducto": search_term,
                    "pagina": 1,
                    "tamanio": 100,
                }
            }

            response = requests.post(self.url, headers=self.headers, json=payload)
            
            if response.status_code == 429:
                raise RateLimitException("Rate limit exceeded")
            
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
        except RateLimitException:
            raise
        except Exception as e:
            print(f"Error fetching search terms data: {e}")
            raise  # Re-raise the exception to be caught by the retry logic

scraper = SearchTermsScraper()
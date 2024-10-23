import requests
import time
from typing import Optional, Dict, Any
from pydantic import BaseModel

class RateLimitException(Exception):
    pass

class ForbiddenException(Exception):
    pass

class MedicineScraper:
    def __init__(self):
        self.url = "https://ms-opm.minsa.gob.pe/msopmcovid/preciovista/ciudadano"
        self.headers = {
            "Origin": "https://opm-digemid.minsa.gob.pe",
            "Referer": "https://opm-digemid.minsa.gob.pe/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
        }
        self.session = requests.Session()

    def search_medicines(self, product_data: Dict[str, Any], region_data: Dict[str, Any], exact_search: bool = False) -> Optional[Dict[str, Any]]:
        try:
            if exact_search:
                nombre_producto = product_data.get('nombreProducto')
            else:
                nombre_producto = None

            payload = {
                "filtro": {
                    "codigoProducto": product_data.get('codigoProducto'),
                    "codigoDepartamento": region_data.get('codigoDepartamento'),
                    "codigoProvincia": region_data.get('codigoProvincia'),
                    "codigoUbigeo": region_data.get('codigoUbigeo'),
                    "codTipoEstablecimiento": None,
                    "catEstablecimiento": None,
                    "codGrupoFF": product_data.get('codGrupoFF'),
                    "concent": product_data.get('concent'),
                    "tamanio": 1000000,
                    "pagina": 1,
                    "nombreProducto": nombre_producto
                }
            }

            response = self.session.post(self.url, headers=self.headers, json=payload)
            
            if response.status_code == 429:
                raise RateLimitException("Rate limit exceeded")
            elif response.status_code == 403:
                raise ForbiddenException("Access forbidden")
            
            response.raise_for_status()
            return response.json()

        except (RateLimitException, ForbiddenException):
            raise
        except Exception as e:
            print(f"Error fetching medicine data: {e}")
            raise

scraper = MedicineScraper()
import requests
import logging
from bs4 import BeautifulSoup
from typing import Optional
from app.models.pharmacy import RawPharmacyData, PharmacySearchRequest, PharmacyResponse

class PharmacyScraper:
    def __init__(self):
        self.base_url = "https://serviciosweb-digemid.minsa.gob.pe/Consultas/Establecimientos"
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://serviciosweb-digemid.minsa.gob.pe/Consultas/Establecimientos",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0.1 Safari/605.1.15",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.logger = logging.getLogger(__name__)

    def search_pharmacies(self, request: PharmacySearchRequest) -> Optional[PharmacyResponse]:
        try:
            params = {
                "accion": "QRY_E",
                "param1": "1",  # 1 for registration number search
                "param2": request.registration_number or "",
                "param3": "",
                "param4": "",
                "param5": "",
                "param6": "",
                "param7": "",
                "param8": "",
                "param9": ""
            }

            self.logger.info(f"Making request to {self.base_url}")
            self.logger.info(f"Parameters: {params}")

            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params
            )
            
            self.logger.info(f"Response status code: {response.status_code}")
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            pharmacies = []

            table = soup.find('table', {'id': 'tresultados'})
            if not table:
                self.logger.error("Could not find results table")
                return PharmacyResponse(coincidencias=0, data=[])

            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) >= 10 and cells[1].text.strip().isdigit():
                    try:
                        pharmacy_data = RawPharmacyData(
                            NroRegistro=cells[2].text.strip(),
                            Categoria=cells[3].text.strip(),
                            NombreComercial=cells[4].text.strip(),
                            RazonSocial=cells[5].text.strip(),
                            RUC=cells[6].text.strip(),
                            Direccion=cells[7].text.strip(),
                            Ubigeo=cells[8].text.strip(),
                            Situacion=cells[9].text.strip(),
                            Empadronado=cells[10].text.strip()
                        )
                        pharmacies.append(pharmacy_data)
                    except Exception as e:
                        self.logger.error(f"Error parsing pharmacy row: {str(e)}")
                        continue

            return PharmacyResponse(
                coincidencias=len(pharmacies),
                data=pharmacies
            )

        except Exception as e:
            self.logger.error(f"Error fetching pharmacy data: {str(e)}")
            self.logger.exception(e)
            return None

scraper = PharmacyScraper()
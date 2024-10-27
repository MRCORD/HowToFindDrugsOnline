import logging
from typing import Optional
from app.models.pharmacy import PharmacySearchRequest, PharmacyResponse
from app.tasks.scrapers.pharmacy_scraper import scraper

class PharmacyService:
    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger(__name__)

    def get_raw_pharmacies(self, search_request: PharmacySearchRequest) -> Optional[PharmacyResponse]:
        try:
            return scraper.search_pharmacies(search_request)
        except Exception as e:
            self.logger.error(f"Error fetching raw pharmacy data: {str(e)}")
            return None
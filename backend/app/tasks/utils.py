import logging

logger = logging.getLogger(__name__)

def setup_logger():
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('scraper.log')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def log_scraping_error(scraper_name, error):
    logger.error(f"Error in {scraper_name}: {str(error)}")

def log_scraping_success(scraper_name, items_count):
    logger.info(f"Successfully scra
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.tasks.scrapers.generics_scraper import scraper as generics_scraper

scheduler = AsyncIOScheduler()

def start_scheduler():
    scheduler.add_job(generics_scraper.scrape_generics, 'cron', hour=0)  # Run daily at midnight
    scheduler.start()
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.tasks.scrapers.generics_scraper import scraper as generics_scraper
from app.services.generics_service import GenericsService
from app.core.database import db

scheduler = AsyncIOScheduler()

def update_all_generics_scheduled():
    generics_service = GenericsService(db)
    generics_service.update_all_generics()

def start_scheduler():
    scheduler.add_job(update_all_generics_scheduled, 'cron', hour=0)  # Run daily at midnight
    scheduler.start()
import requests
from bs4 import BeautifulSoup
from app.core.database import db

class GenericsScraper:
    def __init__(self):
        self.url = "https://example.com/generics"  # Replace with actual URL

    async def scrape_generics(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        generics = []
        for item in soup.find_all('div', class_='generic-item'):
            name = item.find('h2').text.strip()
            description = item.find('p').text.strip()
            generics.append({
                "name": name,
                "description": description
            })
        
        await self.save_to_db(generics)

    async def save_to_db(self, generics):
        await db.generics.insert_many(generics)

scraper = GenericsScraper()
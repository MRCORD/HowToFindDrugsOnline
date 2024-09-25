from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.MONGODB_CONNECTION_STRING)

class Database:
    def __init__(self):
        self.client = client
        self.health = client.get_database("health")
        self.peru = client.get_database("peru")

    def get_database(self, db_name: str):
        return self.client.get_database(db_name)

db = Database()
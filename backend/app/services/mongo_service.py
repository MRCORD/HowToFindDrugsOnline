from typing import Dict, Any, Optional, List
from bson import ObjectId
from app.models.mongo import MongoQuery, ResponseModel

class MongoService:
    def __init__(self, db):
        self.db = db
        self.client = db.client

    def consult_mongo(self, query: MongoQuery) -> ResponseModel:
        database = self.client[query.db]
        collection = database[query.collection]
        
        if query.aggregation:
            cursor = collection.aggregate(query.aggregation)
            documents = list(cursor)
        else:
            cursor = collection.find(query.query).limit(query.limit or 0)
            documents = list(cursor)
        
        documents = [self._convert_objectid(doc) for doc in documents]
        
        return ResponseModel(documents=documents)

    def update_mongo(self, query: MongoQuery) -> Any:
        database = self.client[query.db]
        collection = database[query.collection]
        if not isinstance(query.filter, dict):
            raise TypeError("filter must be an instance of dict")
        return collection.update_one(query.filter, query.update)

    def update_many(self, query: MongoQuery) -> Any:
        """Update multiple documents that match the filter"""
        database = self.client[query.db]
        collection = database[query.collection]
        if not isinstance(query.filter, dict):
            raise TypeError("filter must be an instance of dict")
        return collection.update_many(query.filter, query.update)

    def insert_one(self, document: Dict[str, Any]) -> Any:
        database = self.client[document['db']]
        collection = database[document['collection']]
        return collection.insert_one(document['data'])

    def insert_many(self, documents: Dict[str, Any]) -> Any:
        """Insert many documents at once"""
        database = self.client[documents['db']]
        collection = database[documents['collection']]
        return collection.insert_many(documents['data'])

    def _convert_objectid(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, dict):
            return {k: self._convert_objectid(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_objectid(v) for v in obj]
        else:
            return obj
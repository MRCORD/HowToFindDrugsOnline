from app.models.mongo import MongoQuery, ResponseModel
from bson import ObjectId

class MongoService:
    def __init__(self, db):
        self.db = db

    def consult_mongo(self, query: MongoQuery) -> ResponseModel:
        database = self.db.client[query.db]
        collection = database[query.collection]
        
        if query.aggregation:
            cursor = collection.aggregate(query.aggregation)
            documents = list(cursor)
        else:
            cursor = collection.find(query.query).limit(query.limit or 0)
            documents = list(cursor)
        
        documents = [self._convert_objectid(doc) for doc in documents]
        
        return ResponseModel(documents=documents)

    def _convert_objectid(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, dict):
            return {k: self._convert_objectid(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_objectid(v) for v in obj]
        else:
            return obj
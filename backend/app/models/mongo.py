from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class MongoQuery(BaseModel):
    db: str = Field(..., title="Database name")
    collection: str = Field(..., title="Collection name")
    query: dict = Field(default={}, title="Query parameters")
    limit: Optional[int] = Field(None, title="Limit the number of returned documents")
    aggregation: Optional[List[dict]] = Field(None, title="Aggregation pipeline")

class ResponseModel(BaseModel):
    documents: List[Dict[str, Any]]
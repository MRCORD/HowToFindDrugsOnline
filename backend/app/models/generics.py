from pydantic import BaseModel, Field
from typing import List, Optional

class GenericBase(BaseModel):
    name: str
    description: Optional[str]

class GenericInDB(GenericBase):
    id: str = Field(..., alias="_id")

class GenericCreate(GenericBase):
    pass

class GenericUpdate(GenericBase):
    pass

class GenericResponse(GenericBase):
    id: str
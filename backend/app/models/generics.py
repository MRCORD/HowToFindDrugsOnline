from pydantic import BaseModel
from typing import List
from datetime import datetime

class RawGenericData(BaseModel):
    Cod_Prod: int
    Nom_Prod: str
    concent: str
    Nom_Form_Farm: str
    Presentac: str
    Situacioon: str

class GenericVariation(BaseModel):
    Cod_Prod: int
    concent: str
    Nom_Form_Farm: str
    Presentac: str
    Situacioon: str
    last_modified: datetime = datetime.utcnow()

class GenericProduct(BaseModel):
    product: str
    variations: List[GenericVariation]
    last_updated: datetime = datetime.utcnow()

class UpdateGenericRequest(BaseModel):
    raw_data: List[RawGenericData]
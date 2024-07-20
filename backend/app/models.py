
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class GenericDocument(BaseModel):
    data: Dict[str, Any]

class ResponseModel(BaseModel):
    documents: List[Dict[str, Any]]
    
class ProductData(BaseModel):
    codigoProducto: int = Field(1058, title="Código de producto")
    codGrupoFF: str = Field("3", title="Código de grupo FF")
    concent: str = Field("2mg", title="Concentración")

class RegionData(BaseModel):
    codigoDepartamento: str = Field("15", title="Código de departamento")
    codigoProvincia: str = Field("01", title="Código de provincia")
    codigoUbigeo: str = Field("150109", title="Código de ubigeo")

class MedsRequest(BaseModel):
    product_data: ProductData
    region_data: RegionData
    
class MedsDetailRequest(BaseModel):
    codEstablecimiento: str = Field("0014954", title="Código de establecimiento"),
    codProducto: int = Field(45438, title="Código de producto")
    
class MongoQuery(BaseModel):
    db: str = Field("health", title="Database name")
    collection: str = Field("drugs", title="Collection name")
    query: dict = Field({"searchTerm":"PARACETAMOL", 
                        "comercio.locacion.distrito":"LINCE", 
                        "comercio.codEstab": "0016996"}, title="Query parameters")
    limit: Optional[int] = Field(None, title="Limit the number of returned documents")
    aggregation: Optional[List[dict]] = Field(None, title="Aggregation pipeline")

class UpdateRequest(BaseModel):
    db: str = Field("health", title="Database name")
    collection: str = Field("drugs", title="Collection name")
    query: dict = Field({}, title="Query parameters")
    document: GenericDocument = Field(None, title="Document to update")
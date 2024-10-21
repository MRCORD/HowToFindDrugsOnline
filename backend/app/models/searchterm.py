from pydantic import BaseModel
from typing import Optional

class RawSearchTermData(BaseModel):
    codigoProducto: Optional[str] = None
    nombreProducto: str
    concent: str
    presentacion: Optional[str] = None
    fracciones: Optional[str] = None
    nombreFormaFarmaceutica: str
    nroRegistroSanitario: Optional[str] = None
    titular: Optional[str] = None
    grupo: int
    codGrupoFF: str

class SearchTermRequest(BaseModel):
    search_term: str

class ProcessCatalogRequest(BaseModel):
    limit: Optional[int] = None
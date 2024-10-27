from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class RawPharmacyData(BaseModel):
    NroRegistro: str
    Categoria: str
    NombreComercial: str
    RazonSocial: str
    RUC: str
    Direccion: str
    Ubigeo: str
    Situacion: str
    Empadronado: str

class PharmacySearchRequest(BaseModel):
    registration_number: Optional[str] = None
    name: Optional[str] = None
    ruc: Optional[str] = None

class PharmacyResponse(BaseModel):
    coincidencias: int
    data: List[RawPharmacyData]
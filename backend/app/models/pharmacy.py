from pydantic import BaseModel
from typing import Optional, List, Dict
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

class PharmacyUpdateResult(BaseModel):
    total_unique_codestabs: int
    pharmacies_found: int
    medicines_updated: int
    pharmacies_not_found: int
    not_found_codestabs: List[str]

class PharmacyUpdateStatus(BaseModel):
    status: str = "idle"  # idle, running, completed, failed
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    current_progress: Optional[Dict[str, int]] = None
    error: Optional[str] = None
    result: Optional[PharmacyUpdateResult] = None

class TransformedPharmacyResponse(BaseModel):
    data: List[Dict]

class TransformedPharmacyBatchResponse(BaseModel):
    data: List[Dict]
from pydantic import BaseModel, Field
from typing import List, Optional

class DrugBase(BaseModel):
    searchTerm: str
    concent: str
    nombreFormaFarmaceutica: str

class DrugResponse(DrugBase):
    dropdown: str

class FilteredDrugRequest(BaseModel):
    selected_drug: str = Field(..., example="IBUPROFENO")
    concent: str = Field(..., example="400 mg")
    nombreFormaFarmaceutica: str = Field(..., example="Tableta")
    selected_distrito: str = Field(..., example="MIRAFLORES")

class FilteredDrugResponse(BaseModel):
    nombreProducto: str
    concent: str
    nombreFormaFarmaceutica: str
    precio2: float
    nombreComercial: str
    direccion: str
    googleMaps_search_url: Optional[str] = Field(default="")
    googleMapsUri: Optional[str] = Field(default="")

class FilteredDrugsResponse(BaseModel):
    totalCount: int
    drugs: List[FilteredDrugResponse]
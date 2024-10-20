from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class RawCatalogData(BaseModel):
    Codigo: str = Field(default='')
    Nombre: str = Field(default='')
    Concentracion: str = Field(default='')
    Forma_Farmaceutica: str = Field(default='')
    Presentac: str = Field(default='')
    Fraccion: str = Field(default='')
    Registro_Sanitario: str = Field(default='')
    Nom_Titular: str = Field(default='')
    Laboratorio: str = Field(default='')
    Nom_IFA: str = Field(default='')
    Nom_Rubro: str = Field(default='')
    Situacion: str = Field(default='')
    Fecha_Actualizacion: datetime

    class Config:
        allow_population_by_field_name = True

class CatalogVariation(RawCatalogData):
    last_modified: datetime = Field(default_factory=datetime.utcnow)

class CatalogProduct(BaseModel):
    name: str
    variations: List[CatalogVariation]
    last_updated: datetime = Field(default_factory=datetime.utcnow)

class CatalogResponse(BaseModel):
    update_date: datetime
    data: List[RawCatalogData]

class UpdateCatalogRequest(BaseModel):
    raw_data: List[RawCatalogData]
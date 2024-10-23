from pydantic import BaseModel, Field
from typing import Optional

class ProductData(BaseModel):
    codigoProducto: int = Field(..., description="Product code")
    codGrupoFF: str = Field(..., description="Group code FF")
    concent: str = Field(..., description="Concentration")
    nombreProducto: Optional[str] = Field(None, description="Product name")

class RegionData(BaseModel):
    codigoDepartamento: str = Field(..., description="Department code")
    codigoProvincia: str = Field(..., description="Province code")
    codigoUbigeo: str = Field(..., description="Ubigeo code")

class MedicineSearchRequest(BaseModel):
    product_data: ProductData
    region_data: RegionData
    exact_search: Optional[bool] = Field(False, description="Whether to perform an exact product name match")

class MedicineSearchResponse(BaseModel):
    data: list = Field(..., description="List of medicine search results")
    totalFilas: int = Field(..., description="Total number of rows")
    message: Optional[str] = None
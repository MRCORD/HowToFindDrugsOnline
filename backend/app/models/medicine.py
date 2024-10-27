from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class ProductData(BaseModel):
    codigoProducto: int = Field(..., description="Product code")
    codGrupoFF: str = Field(..., description="Group code FF")
    concent: str = Field(..., description="Concentration")
    nombreProducto: Optional[str] = Field(None, description="Product name")

class RegionData(BaseModel):
    codigoDepartamento: str = Field(..., description="Department code")
    codigoProvincia: str = Field(..., description="Province code")
    codigoUbigeo: Optional[str] = Field(None, description="Ubigeo code")  # Made Optional

class MedicineSearchRequest(BaseModel):
    product_data: ProductData
    region_data: RegionData
    exact_search: Optional[bool] = Field(False, description="Whether to perform an exact product name match")

class MedicineSearchResponse(BaseModel):
    data: list = Field(..., description="List of medicine search results")
    totalFilas: int = Field(..., description="Total number of rows")
    message: Optional[str] = None

class ProcessedMedicine(BaseModel):
    producto: Dict[str, Any] = Field(..., description="Product information")
    comercio: Dict[str, Any] = Field(..., description="Commerce information")
    fecha: str = Field(..., description="Date of record")
    historialPrecios: List[Dict[str, Any]] = Field(default_factory=list, description="Price history")

class ProcessDocumentRequest(BaseModel):
    document_id: str = Field(..., description="ID of the searchterms document to process")
    region_data: RegionData = Field(..., description="Region data for the search")
    limit: Optional[int] = Field(None, description="Limit the number of concentrations to process")
    
class ProcessingRun(BaseModel):
    run_id: str = Field(..., description="Identifier for the processing run")
    status: str = Field(..., description="Overall status: active, completed, failed")
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    region_data: Dict[str, str] = Field(..., description="Region data used for processing")
    processed_ids: List[str] = Field(default_factory=list, description="IDs of successfully processed documents")
    failed_ids: List[str] = Field(default_factory=list, description="IDs of failed documents")
    total_stats: Dict[str, int] = Field(
        default_factory=lambda: {
            "total_documents": 0,
            "processed": 0,
            "successful": 0,
            "failed": 0,
            "skipped": 0,
            "storage": {
                "inserted": 0,
                "updated": 0,
                "unchanged": 0,
                "failed": 0
            }
        }
    )

class ProcessAllRequest(BaseModel):
    region_data: RegionData = Field(..., description="Region data for the search")
    run_id: Optional[str] = Field(None, description="Optional run identifier")
    batch_size: Optional[int] = Field(100, description="Number of documents to process in each batch")
    
class RetryFailedRequest(BaseModel):
    """Request model for retrying failed medicine processing"""
    run_id: str = Field(..., description="Original run ID to retry failed items from")
    region_data: Optional[RegionData] = Field(None, description="Optional override for region data")
    batch_size: Optional[int] = Field(100, description="Number of documents to process in each batch")

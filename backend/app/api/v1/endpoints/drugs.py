from fastapi import APIRouter, Depends, HTTPException
from app.services.drugs_service import DrugsService
from app.models.drugs import FilteredDrugRequest, FilteredDrugsResponse, DrugResponse
from app.api.dependencies import get_drugs_service
from typing import List, Dict

router = APIRouter()

@router.get("/unique_drugs", response_model=List[DrugResponse], tags=["queries", "Production"])
def get_unique_drugs(drugs_service: DrugsService = Depends(get_drugs_service)):
    try:
        return drugs_service.get_unique_drugs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving unique drugs: {str(e)}")

@router.get("/unique_districts", response_model=List[Dict[str, str]], tags=["queries", "Production"])
def get_unique_districts(drugs_service: DrugsService = Depends(get_drugs_service)):
    try:
        return drugs_service.get_unique_districts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving unique districts: {str(e)}")
    
@router.post("/filtered_drugs", response_model=FilteredDrugsResponse, tags=["queries", "Production"])
def get_filtered_drugs(request: FilteredDrugRequest, drugs_service: DrugsService = Depends(get_drugs_service)):
    try:
        return drugs_service.get_filtered_drugs(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving filtered drugs: {str(e)}")

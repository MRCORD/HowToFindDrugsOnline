from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from app.services.pharmacy_service import PharmacyService
from app.models.pharmacy import (
    PharmacySearchRequest, PharmacyResponse, 
    PharmacyUpdateResult, PharmacyUpdateStatus, TransformedPharmacyResponse, TransformedPharmacyBatchResponse
)
from app.api.dependencies import get_pharmacy_service
from typing import List, Dict
from pydantic import BaseModel

router = APIRouter()

class TransformedPharmacyInsertRequest(BaseModel):
    data: List[Dict]

@router.post("/raw", response_model=PharmacyResponse)
def get_raw_pharmacies(
    request: PharmacySearchRequest,
    pharmacy_service: PharmacyService = Depends(get_pharmacy_service)
):
    data = pharmacy_service.get_raw_pharmacies(request)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to fetch pharmacy data")
    return data

@router.post("/transformed", response_model=TransformedPharmacyResponse)
def get_transformed_pharmacies(
    request: PharmacySearchRequest,
    pharmacy_service: PharmacyService = Depends(get_pharmacy_service)
):
    data = pharmacy_service.get_raw_pharmacies(request)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to fetch pharmacy data")
    
    transformed_data = pharmacy_service.transform_pharmacy_data(data)
    return transformed_data

@router.post("/transformed-batch", response_model=TransformedPharmacyBatchResponse)
def get_transformed_pharmacies_batch(
    registration_numbers: List[str],
    pharmacy_service: PharmacyService = Depends(get_pharmacy_service)
):
    transformed_data = pharmacy_service.get_transformed_pharmacies_by_registration_numbers(registration_numbers)
    if not transformed_data:
        raise HTTPException(status_code=500, detail="Failed to fetch transformed pharmacy data")
    return TransformedPharmacyBatchResponse(data=transformed_data)

@router.post("/update-medicine-pharmacy-ids", tags=["admin"])
def start_medicine_pharmacy_ids_update(
    background_tasks: BackgroundTasks,
    pharmacy_service: PharmacyService = Depends(get_pharmacy_service)
):
    """Start the process to update pharmacyId in medicines collection"""
    try:
        message = pharmacy_service.start_medicine_pharmacy_ids_update(background_tasks)
        return {"message": message}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error starting pharmacy IDs update: {str(e)}"
        )

@router.get("/update-status", response_model=PharmacyUpdateStatus, tags=["admin"])
def get_update_status(
    pharmacy_service: PharmacyService = Depends(get_pharmacy_service)
):
    """Get the status of the pharmacy IDs update process"""
    return pharmacy_service.get_update_status()

@router.post("/insert-transformed", tags=["admin"])
def insert_transformed_pharmacies(
    registration_numbers: List[str],
    pharmacy_service: PharmacyService = Depends(get_pharmacy_service)
):
    """Transform and insert an array of pharmacy data into the MongoDB collection"""
    try:
        transformed_data = pharmacy_service.get_transformed_pharmacies_by_registration_numbers(registration_numbers)
        if not transformed_data:
            raise HTTPException(status_code=500, detail="Failed to fetch transformed pharmacy data")
        
        message = pharmacy_service.insert_transformed_pharmacies(transformed_data)
        return {"message": message}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error inserting transformed pharmacy data: {str(e)}"
        )
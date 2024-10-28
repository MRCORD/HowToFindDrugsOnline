from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from app.services.pharmacy_service import PharmacyService
from app.models.pharmacy import (
    PharmacySearchRequest, PharmacyResponse, 
    PharmacyUpdateResult, PharmacyUpdateStatus
)
from app.api.dependencies import get_pharmacy_service

router = APIRouter()

@router.post("/raw", response_model=PharmacyResponse)
def get_raw_pharmacies(
    request: PharmacySearchRequest,
    pharmacy_service: PharmacyService = Depends(get_pharmacy_service)
):
    data = pharmacy_service.get_raw_pharmacies(request)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to fetch pharmacy data")
    return data

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
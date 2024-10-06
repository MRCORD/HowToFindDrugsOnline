from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from app.models.generics import RawGenericData, UpdateGenericRequest
from app.services.generics_service import GenericsService
from app.api.dependencies import get_generics_service
from typing import List, Dict
from threading import Lock

router = APIRouter()

update_status = {"status": "idle", "details": {}}
status_lock = Lock()

@router.get("/raw", response_model=List[RawGenericData])
def get_raw_generics(generics_service: GenericsService = Depends(get_generics_service)):
    return generics_service.get_raw_generics()

@router.get("/")
def get_generics_from_db(generics_service: GenericsService = Depends(get_generics_service)):
    return generics_service.get_generics_from_db()

@router.post("/update")
def update_generics(request: UpdateGenericRequest, generics_service: GenericsService = Depends(get_generics_service)):
    try:
        result = generics_service.update_generics(request.raw_data)
        return {"message": "Generics updated successfully", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update-all")
def update_all_generics(background_tasks: BackgroundTasks, generics_service: GenericsService = Depends(get_generics_service)):
    global update_status
    try:
        with status_lock:
            if update_status["status"] == "in_progress":
                return {"message": "An update is already in progress"}
            update_status = {"status": "in_progress", "details": {}}
        
        background_tasks.add_task(update_all_generics_task, generics_service)
        return {"message": "Update of all generics started in the background"}
    except Exception as e:
        with status_lock:
            update_status = {"status": "failed", "details": {"error": str(e)}}
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/update-status")
def get_update_status():
    global update_status
    with status_lock:
        return update_status

def update_all_generics_task(generics_service: GenericsService):
    global update_status
    try:
        result = generics_service.update_all_generics()
        with status_lock:
            update_status = {"status": "completed", "details": result}
    except Exception as e:
        with status_lock:
            update_status = {"status": "failed", "details": {"error": str(e)}}
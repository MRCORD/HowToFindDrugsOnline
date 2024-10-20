from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from app.models.catalog import RawCatalogData, CatalogResponse, UpdateCatalogRequest
from app.services.catalog_service import CatalogService
from app.api.dependencies import get_catalog_service
from typing import List, Dict, Optional
from threading import Lock

router = APIRouter()

update_status = {"status": "idle", "details": {}}
status_lock = Lock()

@router.get("/raw", response_model=CatalogResponse)
def get_raw_catalog(catalog_service: CatalogService = Depends(get_catalog_service)):
    data = catalog_service.get_raw_catalog()
    if data is None or len(data) == 0:
        raise HTTPException(status_code=500, detail="Failed to fetch catalog data")
    update_date = data[0].Fecha_Actualizacion if data else None
    return CatalogResponse(update_date=update_date, data=data)

@router.get("/raw-excel")
def get_raw_excel(catalog_service: CatalogService = Depends(get_catalog_service)):
    excel_content = catalog_service.get_raw_excel()
    if excel_content is None:
        raise HTTPException(status_code=500, detail="Failed to fetch catalog data")
    return StreamingResponse(
        iter([excel_content.getvalue()]), 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=catalog.xlsx"}
    )

@router.get("/")
def get_catalog_from_db(catalog_service: CatalogService = Depends(get_catalog_service)):
    return catalog_service.get_catalog_from_db()

@router.post("/update")
def update_catalog(request: UpdateCatalogRequest, catalog_service: CatalogService = Depends(get_catalog_service)):
    try:
        result = catalog_service.update_catalog(request.raw_data)
        return {"message": "Catalog updated successfully", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update-all")
def update_all_catalog(background_tasks: BackgroundTasks, catalog_service: CatalogService = Depends(get_catalog_service)):
    global update_status
    try:
        with status_lock:
            if update_status["status"] == "in_progress":
                return {"message": "An update is already in progress"}
            update_status = {"status": "in_progress", "details": {}}
        
        background_tasks.add_task(update_all_catalog_task, catalog_service)
        return {"message": "Update of all catalog items started in the background"}
    except Exception as e:
        with status_lock:
            update_status = {"status": "failed", "details": {"error": str(e)}}
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/update-status")
def get_update_status():
    global update_status
    with status_lock:
        return update_status

def update_all_catalog_task(catalog_service: CatalogService):
    global update_status
    try:
        result = catalog_service.update_all_catalog()
        with status_lock:
            update_status = {"status": "completed", "details": result}
    except Exception as e:
        with status_lock:
            update_status = {"status": "failed", "details": {"error": str(e)}}
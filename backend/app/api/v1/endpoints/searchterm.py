from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from app.models.searchterm import SearchTermRequest, ProcessCatalogRequest
from app.services.searchterm_service import SearchTermService
from app.api.dependencies import get_searchterm_service

router = APIRouter()

@router.post("/raw")
def get_raw_searchterm(request: SearchTermRequest, searchterm_service: SearchTermService = Depends(get_searchterm_service)):
    raw_data = searchterm_service.get_raw_search_terms(request.search_term)
    searchterm_service.process_search_term(request.search_term)
    return raw_data

@router.get("/")
def get_searchterm_from_db(search_term: str = None, searchterm_service: SearchTermService = Depends(get_searchterm_service)):
    return searchterm_service.get_search_terms_from_db(search_term)

@router.post("/process-catalog")
def process_catalog(
    request: ProcessCatalogRequest,
    background_tasks: BackgroundTasks, 
    searchterm_service: SearchTermService = Depends(get_searchterm_service)
):
    background_tasks.add_task(searchterm_service.process_catalog_items, request.limit)
    return {"message": f"Catalog processing started in the background. Limit: {request.limit if request.limit is not None else 'No limit'}"}
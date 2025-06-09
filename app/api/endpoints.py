from fastapi import APIRouter, Query
from app.services.duckduckgo import DuckDuckGoService
from app.services.bing import BingService
from app.models.schema import SearchResult


router = APIRouter()

@router.get("/search/duckduckgo", response_model=SearchResult)
async def search(q: str = Query(..., description="Search in DuckDuckGo for a query")):
    return DuckDuckGoService(q).get_results()

@router.get("/search/bing", response_model=SearchResult)
async def search_bing(q: str = Query(..., description="Search in Bing for a query")):
    return BingService(q).get_results()

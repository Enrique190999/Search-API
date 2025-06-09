from fastapi import APIRouter, Query
from app.services.duckduckgo import DuckDuckGoService
from app.models.schema import SearchResult

router = APIRouter()

@router.get("/search", response_model=SearchResult)
async def search(q: str = Query(..., description="Search in DuckDuckGo for a query")):
    return DuckDuckGoService(q).get_results()

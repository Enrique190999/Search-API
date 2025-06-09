from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from enum import Enum

from app.services.duckduckgo import DuckDuckGoService
from app.services.bing import BingService
from app.models.schema import SearchResult

router = APIRouter()

class SearchEngine(str, Enum):
    duckduckgo = "duckduckgo"
    bing = "bing"

class SearchRequest(BaseModel):
    engine: SearchEngine = Field(..., description="Search engine to use: 'duckduckgo' or 'bing'")
    q: str = Field(..., description="Search query")

@router.post("/search", response_model=SearchResult)
async def search(request: SearchRequest):
    if request.engine == SearchEngine.duckduckgo:
        return DuckDuckGoService(request.q).get_results()
    elif request.engine == SearchEngine.bing:
        return BingService(request.q).get_results()
    else:
        raise HTTPException(status_code=400, detail="Invalid search engine")

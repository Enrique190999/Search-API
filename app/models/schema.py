from pydantic import BaseModel
from typing import List

class ResultItem(BaseModel):
    title: str
    url: str
    description: str

class SearchResult(BaseModel):
    query: str
    wrapper: str
    results: List[ResultItem]

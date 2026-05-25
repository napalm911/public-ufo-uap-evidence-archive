"""Semantic search endpoint."""

from pydantic import BaseModel, Field

from fastapi import APIRouter

from api.services.rag import retrieve

router = APIRouter(prefix="/api", tags=["search"])


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int | None = Field(default=None, ge=1, le=20)
    source: str | None = None


@router.post("/search")
def search(body: SearchRequest):
    results = retrieve(body.query, top_k=body.top_k)
    if body.source:
        results = [r for r in results if r.get("source") == body.source]
    return {"query": body.query, "results": results}

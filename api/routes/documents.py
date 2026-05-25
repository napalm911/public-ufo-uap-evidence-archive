"""Document browse API endpoints."""

from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, Query

from api.lib.labels import source_label, topic_label
from api.services.catalog import (
    filter_files,
    get_extracted_text_path,
    get_file,
    get_timeline,
    get_topics,
)

router = APIRouter(prefix="/api", tags=["documents"])


def _enrich(doc: dict) -> dict:
    return {
        **doc,
        "source_label": source_label(doc.get("source", "")),
        "topic_labels": [topic_label(t) for t in doc.get("topics", [])],
    }


@router.get("/documents")
def list_documents(
    source: str | None = None,
    topic: str | None = None,
    q: str | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    files, total = filter_files(source=source, topic=topic, q=q, limit=limit, offset=offset)
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "files": [_enrich(f) for f in files],
    }


@router.get("/documents/{doc_id:path}/text")
def get_document_text(doc_id: str):
    decoded = unquote(doc_id)
    doc = get_file(decoded)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    txt_path = get_extracted_text_path(doc)
    if not txt_path:
        raise HTTPException(status_code=404, detail="Extracted text not available")

    return {
        "id": doc["id"],
        "path": doc["path"],
        "text": txt_path.read_text(encoding="utf-8", errors="replace"),
    }


@router.get("/documents/{doc_id:path}")
def get_document(doc_id: str):
    decoded = unquote(doc_id)
    doc = get_file(decoded)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return _enrich(doc)


@router.get("/timeline")
def timeline():
    data = get_timeline()
    entries = []
    for entry in data.get("entries", []):
        entries.append(
            {
                **entry,
                "source_label": source_label(entry.get("source", "")),
            }
        )
    return {
        "total_dated_entries": data.get("total_dated_entries", len(entries)),
        "entries": entries,
    }


@router.get("/topics")
def topics():
    topic_list = get_topics()
    return {
        "topics": [
            {"key": t["key"], "label": topic_label(t["key"]), "count": t["count"]}
            for t in topic_list
        ]
    }

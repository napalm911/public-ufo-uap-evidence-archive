"""Archive statistics from metadata."""

import json
from pathlib import Path

from fastapi import APIRouter

from api.config import settings
from api.lib.labels import source_label
from api.services.vector_store import VectorStore

router = APIRouter(prefix="/api", tags=["stats"])


@router.get("/health")
def health():
    store = VectorStore()
    return {
        "status": "ok",
        "indexed_chunks": store.count,
    }


@router.get("/stats")
def stats():
    master_path = settings.metadata_dir / "master_index.json"
    sources = {}
    total_files = 0
    total_sources = 0
    generated = None

    if master_path.exists():
        with open(master_path) as f:
            master = json.load(f)
        total_files = master.get("total_files", 0)
        total_sources = master.get("total_sources", 0)
        generated = master.get("generated")
        for key, info in master.get("sources", {}).items():
            sources[key] = {
                "label": source_label(key),
                "file_count": info.get("file_count", 0),
                "total_size_mb": info.get("total_size_mb", 0),
                "file_types": info.get("file_types", {}),
            }

    store = VectorStore()
    return {
        "total_files": total_files,
        "total_sources": total_sources,
        "generated": generated,
        "indexed_chunks": store.count,
        "sources": sources,
    }

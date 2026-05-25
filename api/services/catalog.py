"""Load and query the file catalog from metadata/files.json."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from api.config import settings


@lru_cache(maxsize=1)
def _load_catalog() -> dict:
    path = settings.metadata_dir / "files.json"
    if not path.exists():
        return {"generated": None, "files": []}
    with open(path) as f:
        return json.load(f)


def reload_catalog():
    _load_catalog.cache_clear()


def all_files() -> list[dict]:
    return _load_catalog().get("files", [])


def get_file(doc_id: str) -> dict | None:
    for f in all_files():
        if f.get("id") == doc_id or f.get("path") == doc_id:
            return f
    return None


def filter_files(
    *,
    source: str | None = None,
    topic: str | None = None,
    q: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> tuple[list[dict], int]:
    files = all_files()

    if source:
        files = [f for f in files if f.get("source") == source]
    if topic:
        files = [f for f in files if topic in f.get("topics", [])]
    if q:
        q_lower = q.lower()
        files = [
            f
            for f in files
            if q_lower in f.get("filename", "").lower()
            or q_lower in f.get("path", "").lower()
        ]

    total = len(files)
    return files[offset : offset + limit], total


def get_timeline() -> dict:
    path = settings.metadata_dir / "timeline.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {"total_dated_entries": 0, "entries": []}


def get_topics() -> list[dict]:
    counts: dict[str, int] = {}
    for f in all_files():
        for topic in f.get("topics", []):
            counts[topic] = counts.get(topic, 0) + 1
    return [{"key": k, "count": v} for k, v in sorted(counts.items(), key=lambda x: -x[1])]


def get_extracted_text_path(doc: dict) -> Path | None:
    """Map data/source/file.pdf -> analysis/extracted_text/source/file.txt"""
    path = doc.get("path", "")
    if not path.startswith("data/"):
        return None
    rel = path[len("data/") :]
    stem = Path(rel).stem
    source = doc.get("source", Path(rel).parts[0] if "/" in rel else "")
    txt_path = settings.extracted_text_dir / source / f"{stem}.txt"
    if txt_path.exists():
        return txt_path
    # also try flat name under source dir
    flat = settings.extracted_text_dir / source / f"{Path(rel).name.replace('.pdf', '.txt').replace('.html', '.txt')}"
    if flat.exists():
        return flat
    return None

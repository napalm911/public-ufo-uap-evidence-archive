"""Tests for document browse API endpoints."""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def client_with_catalog(tmp_path, monkeypatch):
    metadata_dir = tmp_path / "metadata"
    metadata_dir.mkdir()
    data_dir = tmp_path / "data"
    congress = data_dir / "congress"
    congress.mkdir(parents=True)
    pdf = congress / "House_Oversight_UAP_Hearing_20230726.pdf"
    pdf.write_bytes(b"%PDF fake")

    extracted = tmp_path / "analysis" / "extracted_text" / "congress"
    extracted.mkdir(parents=True)
    (extracted / "House_Oversight_UAP_Hearing_20230726.txt").write_text("UAP hearing transcript excerpt.")

    files_catalog = {
        "generated": "2026-01-01T00:00:00",
        "total_files": 1,
        "files": [
            {
                "id": "data/congress/House_Oversight_UAP_Hearing_20230726.pdf",
                "path": "data/congress/House_Oversight_UAP_Hearing_20230726.pdf",
                "filename": "House_Oversight_UAP_Hearing_20230726.pdf",
                "source": "congress",
                "extension": ".pdf",
                "size_bytes": 100,
                "modified": "2026-01-01T00:00:00",
                "topics": ["hearing"],
                "date": "2023-07-26",
            }
        ],
    }
    with open(metadata_dir / "files.json", "w") as f:
        json.dump(files_catalog, f)

    timeline = {
        "total_dated_entries": 1,
        "entries": [
            {
                "date": "2023-07-26",
                "file": "data/congress/House_Oversight_UAP_Hearing_20230726.pdf",
                "source": "congress",
            }
        ],
    }
    with open(metadata_dir / "timeline.json", "w") as f:
        json.dump(timeline, f)

    import api.config as config_module
    import api.services.catalog as catalog_module

    monkeypatch.setattr(config_module.settings, "metadata_dir", metadata_dir)
    monkeypatch.setattr(config_module.settings, "extracted_text_dir", tmp_path / "analysis" / "extracted_text")
    monkeypatch.setattr(config_module.settings, "base_dir", tmp_path)
    catalog_module.reload_catalog()

    def fake_load():
        with open(metadata_dir / "files.json") as f:
            return json.load(f)

    def fake_timeline():
        with open(metadata_dir / "timeline.json") as f:
            return json.load(f)

    def fake_extracted_path(doc: dict):
        rel = doc["path"][len("data/") :]
        source = doc.get("source", rel.split("/")[0])
        stem = Path(rel).stem
        return tmp_path / "analysis" / "extracted_text" / source / f"{stem}.txt"

    monkeypatch.setattr(catalog_module, "_load_catalog", fake_load)
    monkeypatch.setattr(catalog_module, "get_timeline", fake_timeline)
    monkeypatch.setattr(catalog_module, "get_extracted_text_path", fake_extracted_path)

    from api.main import app
    import api.routes.documents as docs_route

    monkeypatch.setattr(docs_route, "get_timeline", fake_timeline)
    monkeypatch.setattr(docs_route, "get_extracted_text_path", fake_extracted_path)

    return TestClient(app)


def test_list_documents(client_with_catalog):
    resp = client_with_catalog.get("/api/documents")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["files"][0]["source_label"] == "Congressional Hearings"


def test_list_documents_by_source(client_with_catalog):
    resp = client_with_catalog.get("/api/documents?source=congress")
    assert resp.status_code == 200
    assert resp.json()["total"] == 1

    resp = client_with_catalog.get("/api/documents?source=fbi")
    assert resp.json()["total"] == 0


def test_get_document(client_with_catalog):
    doc_id = "data/congress/House_Oversight_UAP_Hearing_20230726.pdf"
    resp = client_with_catalog.get(f"/api/documents/{doc_id}")
    assert resp.status_code == 200
    assert resp.json()["filename"] == "House_Oversight_UAP_Hearing_20230726.pdf"


def test_get_document_text(client_with_catalog):
    doc_id = "data/congress/House_Oversight_UAP_Hearing_20230726.pdf"
    resp = client_with_catalog.get(f"/api/documents/{doc_id}/text")
    assert resp.status_code == 200
    assert "UAP hearing" in resp.json()["text"]


def test_timeline(client_with_catalog):
    resp = client_with_catalog.get("/api/timeline")
    assert resp.status_code == 200
    assert resp.json()["total_dated_entries"] == 1


def test_topics(client_with_catalog):
    resp = client_with_catalog.get("/api/topics")
    assert resp.status_code == 200
    topics = resp.json()["topics"]
    assert any(t["key"] == "hearing" for t in topics)

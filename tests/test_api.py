"""Tests for FastAPI endpoints."""

from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from api.main import app
    return TestClient(app)


def test_health(client):
    with patch("api.routes.stats.VectorStore") as MockStore:
        MockStore.return_value.count = 42
        resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["indexed_chunks"] == 42


def test_stats(client):
    resp = client.get("/api/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert "total_files" in data
    assert "sources" in data
    assert "indexed_chunks" in data


def test_search(client):
    mock_results = [
        {
            "text": "UAP assessment excerpt",
            "source": "odni",
            "filename": "odni_sample.txt",
            "chunk_index": 0,
            "topics": "",
            "score": 0.92,
        }
    ]
    with patch("api.routes.search.retrieve", return_value=mock_results):
        resp = client.post("/api/search", json={"query": "UAP assessment"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["query"] == "UAP assessment"
    assert len(data["results"]) == 1


def test_chat_non_streaming(client):
    mock_response = {
        "answer": "Based on the ODNI report, UAP remain unexplained in many cases.",
        "sources": [{"text": "excerpt", "source": "odni", "filename": "report.txt", "score": 0.9}],
    }
    with patch("api.routes.chat.chat_sync", return_value=mock_response):
        resp = client.post("/api/chat", json={"message": "What did ODNI conclude?", "stream": False})
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    assert len(data["sources"]) == 1


def test_chat_missing_message(client):
    resp = client.post("/api/chat", json={"message": "", "stream": False})
    assert resp.status_code == 422

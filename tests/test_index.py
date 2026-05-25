"""Tests for vector index building."""

import importlib
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parent.parent
FIXTURE_TEXT = ROOT / "tests" / "fixtures" / "extracted_text" / "demo"


def test_build_index_dry_run():
    import scripts.build_index as bi

    summary = bi.build_index(FIXTURE_TEXT, dry_run=True)
    assert summary["files_processed"] >= 3
    assert summary["chunks_created"] > 0
    assert "demo" in summary["sources"]


def test_build_index_with_mocked_embeddings(tmp_chroma_path):
    import api.config as config_module
    importlib.reload(config_module)

    import scripts.build_index as bi

    fake_embeddings = [[0.1] * 384]

    with patch("api.services.vector_store.embed_texts") as mock_embed:
        mock_embed.side_effect = lambda texts: [fake_embeddings[0] for _ in texts]

        summary = bi.build_index(FIXTURE_TEXT, force=True, dry_run=False)
        assert summary["chunks_created"] > 0
        assert summary.get("indexed_chunks", 0) == summary["chunks_created"]

        from api.services.vector_store import VectorStore

        store = VectorStore()
        assert store.count == summary["chunks_created"]

        results = store.search("UAP preliminary assessment")
        assert len(results) >= 1
        assert "text" in results[0]

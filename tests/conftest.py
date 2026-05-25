"""Pytest configuration and shared fixtures."""

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


@pytest.fixture
def tmp_chroma_path(tmp_path, monkeypatch):
    chroma = tmp_path / "vector_store"
    monkeypatch.setenv("CHROMA_PATH", str(chroma))
    monkeypatch.setenv("EMBEDDING_PROVIDER", "local")
    # Reload settings after env change
    import importlib
    import api.config as config_module
    importlib.reload(config_module)
    return chroma

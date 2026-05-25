"""Tests for configuration loading."""

import importlib
import os


def test_settings_defaults(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.setenv("CHUNK_SIZE", "500")

    import api.config as config_module
    importlib.reload(config_module)

    assert config_module.settings.chunk_size == 500
    assert config_module.settings.deepseek_base_url == "https://api.deepseek.com"
    assert config_module.settings.embedding_provider == "local"


def test_cors_origins_parsed(monkeypatch):
    monkeypatch.setenv("CORS_ORIGINS", "http://a.test,http://b.test")

    import api.config as config_module
    importlib.reload(config_module)

    assert "http://a.test" in config_module.settings.cors_origins
    assert "http://b.test" in config_module.settings.cors_origins

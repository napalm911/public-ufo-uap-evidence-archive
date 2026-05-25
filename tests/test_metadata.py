"""Tests for metadata generation."""

import json
import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def test_generate_metadata_with_fixture_data(tmp_path, monkeypatch):
    """Run metadata generation against a minimal fixture data dir."""
    data_dir = tmp_path / "data"
    metadata_dir = tmp_path / "metadata"

    # Create minimal fixture structure
    demo = data_dir / "demo"
    demo.mkdir(parents=True)
    (demo / "sample.pdf").write_bytes(b"%PDF-1.4 fake content for testing")

    # Patch paths in generate_metadata module
    import scripts.generate_metadata as gm

    monkeypatch.setattr(gm, "DATA_DIR", data_dir)
    monkeypatch.setattr(gm, "METADATA_DIR", metadata_dir)
    monkeypatch.setattr(gm, "BASE_DIR", tmp_path)

    catalog = gm.scan_all_files()
    assert len(catalog["all_files"]) == 1
    assert "demo" in catalog["by_source"]

    gm.main()

    master_path = metadata_dir / "master_index.json"
    assert master_path.exists()
    with open(master_path) as f:
        master = json.load(f)
    assert master["total_files"] == 1
    assert "demo" in master["sources"]

    assert (metadata_dir / "timeline.json").exists()
    assert (metadata_dir / "topic_tags.json").exists()
    assert (metadata_dir / "source_index.json").exists()

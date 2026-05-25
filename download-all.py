#!/usr/bin/env python3
"""
Public UFO/UAP Evidence Archive - Main Downloader

Downloads all publicly available U.S. government UFO/UAP documents
from official sources. Run this to populate the data/ directory.

Usage:
    python download-all.py                  # Download all sources
    python download-all.py --source fbi     # Download specific source
    python download-all.py --list           # List available sources
    python download-all.py --metadata-only  # Only build metadata indexes
"""

import argparse
import importlib
import json
import os
import sys
from pathlib import Path

SOURCES = {
    "fbi": {"module": "sources.fbi_vault", "desc": "FBI Vault - UFO Files"},
    "cia-crest": {"module": "sources.cia_crest", "desc": "CIA CREST Archive (UFO-related docs)"},
    "blue-book": {"module": "sources.project_blue_book", "desc": "Project Blue Book (National Archives)"},
    "odni": {"module": "sources.odni_report", "desc": "ODNI UAP Preliminary Assessment 2021"},
    "aaro": {"module": "sources.aaro", "desc": "AARO Historical Record Reports"},
    "nasa": {"module": "sources.nasa_uap", "desc": "NASA UAP Independent Study"},
    "navy-videos": {"module": "sources.navy_videos", "desc": "U.S. Navy UAP Videos (DoD-confirmed)"},
    "pentagon": {"module": "sources.pentagon_briefings", "desc": "Pentagon AARO Briefings & Testimony"},
    "disclosure-act": {"module": "sources.disclosure_act", "desc": "UAP Disclosure Act / NDAA Language"},
    "foia": {"module": "sources.foia_collections", "desc": "FOIA Collections Index (Black Vault)"},
    "doe": {"module": "sources.doe_nnsa", "desc": "DOE/NNSA Documents"},
    "congress": {"module": "sources.congressional_hearings", "desc": "Congressional UAP Hearings Transcripts"},
    "foreign": {"module": "sources.foreign_releases", "desc": "Foreign Government Releases"},
}

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"
METADATA_DIR = BASE_DIR / "metadata"


def list_sources():
    print(f"\n{'Source':<20} Description")
    print("-" * 60)
    for key, info in sorted(SOURCES.items()):
        print(f"{key:<20} {info['desc']}")
    print()


def run_source(key, info):
    print(f"\n{'='*60}")
    print(f"Downloading: {info['desc']} ({key})")
    print(f"{'='*60}")
    try:
        module = importlib.import_module(info["module"])
        source_dir = DATA_DIR / key.replace("-", "_")
        source_dir.mkdir(parents=True, exist_ok=True)
        if hasattr(module, "download"):
            result = module.download(str(source_dir))
            if result:
                print(f"  ✓ Completed: {result}")
            else:
                print(f"  ✓ Source completed")
        else:
            print(f"  ⚠ No download() function found in {info['module']}")
    except Exception as e:
        print(f"  ✗ Error: {e}", file=sys.stderr)


def build_metadata_index():
    """Generate full metadata indexes via scripts/generate_metadata.py."""
    import subprocess
    script = BASE_DIR / "scripts" / "generate_metadata.py"
    print("\nBuilding metadata indexes...")
    result = subprocess.run([sys.executable, str(script)], cwd=str(BASE_DIR))
    if result.returncode != 0:
        sys.exit(result.returncode)
    index_path = METADATA_DIR / "master_index.json"
    if index_path.exists():
        with open(index_path) as f:
            return json.load(f)
    return {}


def main():
    parser = argparse.ArgumentParser(description="Download UFO/UAP evidence archive")
    parser.add_argument("--source", "-s", help="Download a specific source (omit for all)")
    parser.add_argument("--list", "-l", action="store_true", help="List available sources")
    parser.add_argument("--metadata-only", action="store_true", help="Only rebuild metadata index")
    args = parser.parse_args()
    
    if args.list:
        list_sources()
        return
    
    if args.metadata_only:
        build_metadata_index()
        return
    
    if args.source:
        if args.source not in SOURCES:
            print(f"Unknown source: {args.source}")
            print(f"Available: {', '.join(sorted(SOURCES.keys()))}")
            sys.exit(1)
        run_source(args.source, SOURCES[args.source])
    else:
        for key, info in sorted(SOURCES.items()):
            run_source(key, info)
    
    # Build metadata after downloads
    build_metadata_index()
    print("\n✓ All done!")


if __name__ == "__main__":
    main()

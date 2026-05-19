#!/usr/bin/env python3
"""
Source: FBI Vault - UFO Files
URL: https://vault.fbi.gov/UFO

The FBI's declassified UFO-related files, including the famous
Hottel memo (1947) and thousands of pages of investigation records.
"""

import json
import os
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://vault.fbi.gov"
COLLECTION_URL = f"{BASE_URL}/UFO"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
DELAY = 2.0  # Be polite to gov servers


def download(output_dir: str) -> dict:
    """Download FBI Vault UFO files."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"  Fetching FBI Vault UFO collection index...")
    
    # Create a metadata file documenting what's available
    entries = []
    try:
        resp = requests.get(COLLECTION_URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        
        # Find PDF links in the FBI Vault listing
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.endswith(".pdf") or "download" in href:
                full_url = href if href.startswith("http") else f"{BASE_URL}{href}"
                entries.append({
                    "url": full_url,
                    "title": link.get_text(strip=True) or Path(href).name,
                    "filename": Path(href).name,
                })
    except Exception as e:
        print(f"  ⚠ Could not fetch live index: {e}")
        # Provide a fallback with known FBI UFO files
        entries = _known_fbi_ufo_files()
    
    # Write metadata index
    index = {
        "source": "FBI Vault - UFO Files",
        "url": COLLECTION_URL,
        "count": len(entries),
        "entries": entries,
    }
    with open(output_path / "_index.json", "w") as f:
        json.dump(index, f, indent=2)
    
    print(f"  Indexed {len(entries)} FBI UFO document entries")
    
    # Download each PDF
    downloaded = 0
    for entry in entries:
        local_path = output_path / entry["filename"]
        if local_path.exists() and local_path.stat().st_size > 0:
            continue  # Already downloaded
        
        try:
            resp = requests.get(entry["url"], headers=HEADERS, timeout=60)
            resp.raise_for_status()
            local_path.write_bytes(resp.content)
            downloaded += 1
            print(f"    ✓ {entry['filename']}")
            time.sleep(DELAY)
        except Exception as e:
            print(f"    ✗ {entry['filename']}: {e}")
    
    print(f"  Downloaded: {downloaded} new files")
    summary_file = output_path / "_summary.json"
    with open(summary_file, "w") as f:
        json.dump({"downloaded": downloaded, "total_indexed": len(entries)}, f)
    
    return {"downloaded": downloaded, "total": len(entries)}


def _known_fbi_ufo_files() -> list:
    """Fallback list of known FBI UFO files if the vault is unreachable."""
    return [
        {
            "url": "https://vault.fbi.gov/UFO/UFO%20Part%201%20of%202/view",
            "title": "UFO File - Part 1 of 2",
            "filename": "fbi_ufo_part1.pdf",
        },
        {
            "url": "https://vault.fbi.gov/UFO/UFO%20Part%202%20of%202/view",
            "title": "UFO File - Part 2 of 2",
            "filename": "fbi_ufo_part2.pdf",
        },
    ]

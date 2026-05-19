#!/usr/bin/env python3
"""
Source: Project Blue Book - U.S. Air Force (National Archives)
URL: https://www.archives.gov/research/military/air-force/blue-book

All 12,600+ reports from the U.S. Air Force's Project Blue Book (1947-1969).
The lion's share of U.S. government UFO investigation data.
"""

import json
from pathlib import Path

import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

# National Archives Project Blue Book - bulk available via NARA catalog
# The complete Blue Book collection can be accessed through NARA's catalog API
NARA_API = "https://catalog.archives.gov/api/v1"
BLUE_BOOK_NA_ID = 595576  # National Archives Identifier for Project Blue Book

FILES = [
    {
        "url": "https://www.archives.gov/files/research/military/air-force/blue-book/blue-book-report.pdf",
        "filename": "Project_Blue_Book_Final_Report.pdf",
        "title": "Project Blue Book Final Report (Air Force summary)",
        "type": "report",
    },
    {
        "url": "https://www.archives.gov/research/military/air-force/blue-book",
        "filename": "_nara_guide.html",
        "title": "NARA Project Blue Book Research Guide",
        "type": "guide",
        "save_as_html": True,
    },
]


def download(output_dir: str) -> dict:
    """Download Project Blue Book resources."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    results = []
    
    for file_info in FILES:
        local_path = output_path / file_info["filename"]
        
        if local_path.exists() and local_path.stat().st_size > 0:
            print(f"  ✓ {file_info['filename']} (already exists)")
            results.append({"file": file_info["filename"], "status": "exists"})
            continue
        
        try:
            print(f"  Downloading {file_info['filename']}...", end=" ", flush=True)
            resp = requests.get(file_info["url"], headers=HEADERS, timeout=60)
            resp.raise_for_status()
            
            if file_info.get("save_as_html"):
                local_path.write_text(resp.text)
            else:
                local_path.write_bytes(resp.content)
            
            print(f"✓ ({len(resp.content)} bytes)")
            results.append({"file": file_info["filename"], "status": "downloaded", "size": len(resp.content)})
        except Exception as e:
            print(f"✗ {e}")
            results.append({"file": file_info["filename"], "status": "error", "error": str(e)})
    
    # Fetch NARA catalog metadata
    try:
        print(f"  Fetching NARA catalog entry for Project Blue Book...", end=" ", flush=True)
        resp = requests.get(
            f"{NARA_API}/id/{BLUE_BOOK_NA_ID}",
            headers=HEADERS,
            timeout=30,
        )
        resp.raise_for_status()
        nara_data = resp.json()
        with open(output_path / "_nara_catalog.json", "w") as f:
            json.dump(nara_data, f, indent=2)
        print("✓")
    except Exception as e:
        print(f"  ⚠ Could not fetch NARA catalog: {e}")
    
    # Write index
    with open(output_path / "_index.json", "w") as f:
        meta = {
            "source": "Project Blue Book - U.S. Air Force",
            "nara_id": BLUE_BOOK_NA_ID,
            "total_reports": "12,600+",
            "time_period": "1947-1969",
            "url": "https://www.archives.gov/research/military/air-force/blue-book",
            "files": FILES,
            "results": results,
            "note": "Full 12,600+ case files available via NARA. Use the provided NARA ID to query the catalog API for bulk download.",
        }
        json.dump(meta, f, indent=2)
    
    return {"downloaded": sum(1 for r in results if r["status"] == "downloaded"), "total": len(FILES)}

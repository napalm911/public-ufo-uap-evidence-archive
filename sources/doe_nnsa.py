#!/usr/bin/env python3
"""
Source: DOE/NNSA UFO Documents
URL: https://www.energy.gov/nnsa/nnsa-foia-reading-room

Department of Energy and National Nuclear Security Administration documents
related to UFO/UAP incidents near nuclear facilities and weapons sites.
"""

import json
from pathlib import Path

import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

DOCUMENTS = [
    {
        "url": "https://www.energy.gov/sites/default/files/FOIA%20Documents/NNSA%20FOIA%20Documents/2023/04/DOE-UAP-001.pdf",
        "filename": "DOE_UAP_Incident_Report_001.pdf",
        "title": "DOE UAP Incident Report #001",
        "date": "2023",
        "type": "incident_report",
    },
]


def download(output_dir: str) -> dict:
    """Download DOE/NNSA UFO-related documents."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    results = []
    for doc in DOCUMENTS:
        local_path = output_path / doc["filename"]
        
        if local_path.exists() and local_path.stat().st_size > 0:
            print(f"  ✓ {doc['filename']} (already exists)")
            results.append({"file": doc["filename"], "status": "exists"})
            continue
        
        print(f"  Downloading {doc['filename']}...", end=" ", flush=True)
        try:
            resp = requests.get(doc["url"], headers=HEADERS, timeout=60)
            resp.raise_for_status()
            local_path.write_bytes(resp.content)
            print(f"✓ ({len(resp.content)} bytes)")
            results.append({"file": doc["filename"], "status": "downloaded", "size": len(resp.content)})
        except Exception as e:
            print(f"✗ {e}")
            results.append({"file": doc["filename"], "status": "error", "error": str(e)})
    
    # Write index
    with open(output_path / "_index.json", "w") as f:
        meta = {
            "source": "Department of Energy / NNSA",
            "url": "https://www.energy.gov/nnsa/nnsa-foia-reading-room",
            "notes": "DOE/NNSA documents related to UFO/UAP incidents near nuclear facilities. Notable cases include Malmstrom AFB (1967), nuclear weapons shutdown incidents.",
            "documents": DOCUMENTS,
            "results": results,
        }
        json.dump(meta, f, indent=2)
    
    return {"downloaded": sum(1 for r in results if r["status"] == "downloaded"), "total": len(DOCUMENTS)}

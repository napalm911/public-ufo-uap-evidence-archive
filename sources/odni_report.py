#!/usr/bin/env python3
"""
Source: ODNI UAP Preliminary Assessment (June 2021)
URL: https://www.dni.gov/files/ODNI/documents/assessments/Preliminary-Assessment-UAP-20210625.pdf

The landmark 2021 report mandated by the FY2021 Intelligence Authorization Act
(signed by Trump in Dec 2020). This is the first official U.S. intelligence
assessment on UAPs.
"""

import json
import time
from pathlib import Path

import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

FILES = [
    {
        "url": "https://www.dni.gov/files/ODNI/documents/assessments/Preliminary-Assessment-UAP-20210625.pdf",
        "filename": "ODNI_Preliminary_Assessment_UAP_20210625.pdf",
        "title": "Preliminary Assessment on Unidentified Aerial Phenomena (June 2021)",
        "type": "report",
    },
    {
        "url": "https://www.dni.gov/files/ODNI/documents/assessments/Preliminary-Assessment-UAP-20210625-508.pdf",
        "filename": "ODNI_Preliminary_Assessment_UAP_20210625_508.pdf",
        "title": "Preliminary Assessment on UAP (508 Compliant Version)",
        "type": "report",
    },
]


def download(output_dir: str) -> dict:
    """Download ODNI UAP Preliminary Assessment PDFs."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    results = []
    for file_info in FILES:
        local_path = output_path / file_info["filename"]
        
        if local_path.exists() and local_path.stat().st_size > 0:
            print(f"  ✓ {file_info['filename']} (already exists)")
            results.append({"file": file_info["filename"], "status": "exists"})
            continue
        
        print(f"  Downloading {file_info['filename']}...", end=" ", flush=True)
        try:
            resp = requests.get(file_info["url"], headers=HEADERS, timeout=60)
            resp.raise_for_status()
            local_path.write_bytes(resp.content)
            print(f"✓ ({len(resp.content)} bytes)")
            results.append({"file": file_info["filename"], "status": "downloaded", "size": len(resp.content)})
            time.sleep(1)
        except Exception as e:
            print(f"✗ {e}")
            results.append({"file": file_info["filename"], "status": "error", "error": str(e)})
    
    # Write metadata
    with open(output_path / "_index.json", "w") as f:
        meta = {
            "source": "ODNI - Office of the Director of National Intelligence",
            "notes": "Mandated by FY2021 Intelligence Authorization Act. Signed into law by President Trump Dec 2020.",
            "files": FILES,
            "results": results,
        }
        json.dump(meta, f, indent=2)
    
    return {"downloaded": sum(1 for r in results if r["status"] == "downloaded"), "total": len(FILES)}

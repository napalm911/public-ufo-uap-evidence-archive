#!/usr/bin/env python3
"""
Source: UAP Disclosure Act & NDAA Language
URL: https://www.congress.gov/

Legislative text related to UAP disclosure, including the UAP Disclosure Act
of 2023 (Schumer-Rounds amendment) and related NDAA provisions.
"""

import json
from pathlib import Path

import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

DOCUMENTS = [
    {
        "url": "https://www.congress.gov/117/plaws/publ263/PLAW-117publ263.pdf",
        "filename": "NDAA_FY2023_UAP_Provisions.pdf",
        "title": "NDAA FY2023 - UAP Amendment Provisions",
        "date": "2022-12-23",
        "type": "legislation",
    },
    {
        "url": "https://www.congress.gov/118/plaws/publ50/PLAW-118publ50.pdf",
        "filename": "NDAA_FY2024_UAP_Provisions.pdf",
        "title": "NDAA FY2024 - UAP Disclosure Act Provisions",
        "date": "2023-12-22",
        "type": "legislation",
    },
    {
        "url": "https://www.rubio.senate.gov/wp-content/uploads/UAPDA.pdf",
        "filename": "UAP_Disclosure_Act_Full_Text_2023.pdf",
        "title": "UAP Disclosure Act of 2023 (Schumer-Rounds) - Full Text",
        "date": "2023-07-13",
        "type": "legislation",
    },
]


def download(output_dir: str) -> dict:
    """Download UAP-related legislation text."""
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
            resp = requests.get(doc["url"], headers=HEADERS, timeout=60, allow_redirects=True)
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
            "source": "U.S. Congress",
            "url": "https://www.congress.gov/",
            "notes": "Includes the Schumer-Rounds UAP Disclosure Act (July 2023) and UAP-related provisions in FY2023 and FY2024 NDAAs.",
            "documents": DOCUMENTS,
            "results": results,
        }
        json.dump(meta, f, indent=2)
    
    return {"downloaded": sum(1 for r in results if r["status"] == "downloaded"), "total": len(DOCUMENTS)}

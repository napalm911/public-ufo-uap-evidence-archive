#!/usr/bin/env python3
"""
Source: CIA CREST Archive (UFO-related records)
URL: https://www.cia.gov/readingroom/collection/crest-25-year-program-archive

The CIA's CREST (CREST: CIA Records Search Tool) 25-Year Program Archive
contains declassified CIA documents, including known UFO/UAP-related records.
"""

import json
from pathlib import Path

import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

# Key known CIA UFO/UAP-related documents from the CREST archive
# (document IDs from the CIA reading room)
KNOWN_DOCUMENTS = [
    {
        "url": "https://www.cia.gov/readingroom/docs/CIA-RDP80B01676R001000130004-8.pdf",
        "filename": "CIA_UFO_Briefing_1952.pdf",
        "title": "CIA Briefing on UFOs - OSI Report (1952)",
        "date": "1952",
        "type": "briefing",
    },
    {
        "url": "https://www.cia.gov/readingroom/docs/CIA-RDP81R00560R000100010003-8.pdf",
        "filename": "CIA_OSI_UFO_Assessment_1960.pdf",
        "title": "CIA Office of Scientific Intelligence - UFO Assessment",
        "date": "1960",
        "type": "assessment",
    },
    {
        "url": "https://www.cia.gov/readingroom/docs/CIA-RDP86-00513R006300040069-4.pdf",
        "filename": "CIA_ATIP_UFO_1975.pdf",
        "title": "CIA - Advanced Technology Intelligence on UFOs (1975)",
        "date": "1975",
        "type": "report",
    },
    {
        "url": "https://www.cia.gov/readingroom/docs/CIA-RDP79-00849A000400020002-5.pdf",
        "filename": "CIA_OSI_UAP_Study_1978.pdf",
        "title": "CIA OSI Study on Aerial Phenomena (1978)",
        "date": "1978",
        "type": "study",
    },
    {
        "url": "https://www.cia.gov/readingroom/docs/CIA-RDP96-00788R001700210019-4.pdf",
        "filename": "CIA_Stargate_UFO_References.pdf",
        "title": "CIA Stargate Program - UFO-related documents",
        "date": "1980s",
        "type": "stargate",
    },
]


def download(output_dir: str) -> dict:
    """Download known CIA CREST UFO documents."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    results = []
    for doc in KNOWN_DOCUMENTS:
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
            "source": "CIA CREST (25-Year Program Archive)",
            "url": "https://www.cia.gov/readingroom/collection/crest-25-year-program-archive",
            "notes": "The CREST archive contains over 13 million pages of declassified CIA documents. These are the known UFO/UAP-related documents. The search query 'ufo' returns hundreds of additional results on the CIA reading room.",
            "documents": KNOWN_DOCUMENTS,
            "results": results,
            "search_query": "https://www.cia.gov/readingroom/search/site/ufo",
        }
        json.dump(meta, f, indent=2)
    
    return {"downloaded": sum(1 for r in results if r["status"] == "downloaded"), "total": len(KNOWN_DOCUMENTS)}

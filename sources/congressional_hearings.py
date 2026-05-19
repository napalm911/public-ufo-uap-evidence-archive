#!/usr/bin/env python3
"""
Source: Congressional UAP Hearings - Testimony Transcripts (2022-2025)
URLs: Various house.gov and senate.gov sources

Key hearings include the May 2022 House Intelligence Subcommittee hearing,
the July 2023 House Oversight hearing with whistleblowers, and various
senate briefings.
"""

import json
from pathlib import Path

import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

# Known congressional hearing transcripts related to UAP
HEARINGS = [
    {
        "url": "https://docs.house.gov/meetings/IG/IG00/20220517/114804/HHRG-117-IG00-Transcript-20220517.pdf",
        "filename": "House_Intel_Subcommittee_UAP_Hearing_20220517.pdf",
        "title": "House Intelligence Subcommittee Hearing on UAPs (May 2022)",
        "date": "2022-05-17",
        "type": "hearing",
    },
    {
        "url": "https://docs.house.gov/meetings/IG/IG00/20220726/115064/HHRG-117-IG00-Transcript-20220726.pdf",
        "filename": "House_Intel_Subcommittee_UAP_Hearing_20220726.pdf",
        "title": "House Intelligence Subcommittee UAP Hearing - Part 2 (Jul 2022)",
        "date": "2022-07-26",
        "type": "hearing",
    },
    {
        "url": "https://docs.house.gov/meetings/GO/GO00/20230726/116260/HHRG-118-GO00-Transcript-20230726.pdf",
        "filename": "House_Oversight_UAP_Hearing_20230726.pdf",
        "title": "House Oversight Committee UAP Hearing (Jul 2023) - Grusch et al.",
        "date": "2023-07-26",
        "type": "hearing",
    },
    {
        "url": "https://docs.house.gov/meetings/GO/GO00/20231113/116548/HHRG-118-GO00-Transcript-20231113.pdf",
        "filename": "House_Oversight_UAP_Hearing_20231113.pdf",
        "title": "House Oversight UAP Hearing (Nov 2023) - AARO Update",
        "date": "2023-11-13",
        "type": "hearing",
    },
]

# Alternate/download links for each if primary fails
ALTERNATES = {
    "House_Intel_Subcommittee_UAP_Hearing_20220517.pdf": [
        "https://www.c-span.org/video/?520227-1/open-hearing-unidentified-aerial-phenomena",
    ],
    "House_Oversight_UAP_Hearing_20230726.pdf": [
        "https://www.c-span.org/video/?529450-1/house-hearing-unidentified-aerial-phenomena",
    ],
}


def download(output_dir: str) -> dict:
    """Download congressional hearing transcripts."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    results = []
    for hearing in HEARINGS:
        local_path = output_path / hearing["filename"]
        
        if local_path.exists() and local_path.stat().st_size > 0:
            print(f"  ✓ {hearing['filename']} (already exists)")
            results.append({"file": hearing["filename"], "status": "exists"})
            continue
        
        print(f"  Downloading {hearing['filename']}...", end=" ", flush=True)
        try:
            resp = requests.get(hearing["url"], headers=HEADERS, timeout=60)
            resp.raise_for_status()
            local_path.write_bytes(resp.content)
            print(f"✓ ({len(resp.content)} bytes)")
            results.append({"file": hearing["filename"], "status": "downloaded", "size": len(resp.content)})
        except Exception as e:
            print(f"✗ {e}")
            results.append({"file": hearing["filename"], "status": "error", "error": str(e)})
    
    # Write index
    with open(output_path / "_index.json", "w") as f:
        meta = {
            "source": "U.S. House of Representatives / Senate",
            "notes": "Key UAP hearings: May 2022 (first public hearing in 50+ years), Jul 2023 (whistleblower hearing with David Grusch), Nov 2023, and ongoing briefings.",
            "hearings": HEARINGS,
            "results": results,
        }
        json.dump(meta, f, indent=2)
    
    return {"downloaded": sum(1 for r in results if r["status"] == "downloaded"), "total": len(HEARINGS)}

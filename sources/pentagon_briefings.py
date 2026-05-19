#!/usr/bin/env python3
"""
Source: Pentagon Briefings & Press Releases on UAP
URL: https://www.defense.gov/

Official DoD press releases, AARO briefings, and Pentagon press secretary
comments on UAP activities.
"""

import json
from pathlib import Path

import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

DOCUMENTS = [
    {
        "url": "https://www.defense.gov/News/Releases/Release/Article/2169488/statement-by-the-department-of-defense-on-the-release-of-historical-na/",
        "filename": "_DoD_UAP_Video_Release_20200427.html",
        "title": "DoD Statement on Release of UAP Videos (Apr 2020)",
        "date": "2020-04-27",
        "type": "press_release",
        "save_as_html": True,
    },
    {
        "url": "https://www.defense.gov/News/Releases/Release/Article/3100031/dod-announces-the-establishment-of-the-all-domain-anomaly-resolution-o/",
        "filename": "_DoD_AARO_Establishment_20220720.html",
        "title": "DoD Announces Establishment of AARO (Jul 2022)",
        "date": "2022-07-20",
        "type": "press_release",
        "save_as_html": True,
    },
    {
        "url": "https://www.defense.gov/News/Releases/Release/Article/3601002/dod-announces-the-release-of-the-historical-record-report-volume-1/",
        "filename": "_DoD_AARO_HRR_Vol1_Release_20240308.html",
        "title": "DoD Announces Release of AARO HRR Vol 1 (Mar 2024)",
        "date": "2024-03-08",
        "type": "press_release",
        "save_as_html": True,
    },
    {
        "url": "https://www.defense.gov/News/Releases/Release/Article/3955972/dod-announces-the-release-of-the-historical-record-report-volume-2/",
        "filename": "_DoD_AARO_HRR_Vol2_Release_20241114.html",
        "title": "DoD Announces Release of AARO HRR Vol 2 (Nov 2024)",
        "date": "2024-11-14",
        "type": "press_release",
        "save_as_html": True,
    },
    {
        "url": "https://www.aaro.mil/Resources/Speeches/Speech/Article/3490299/subcommittee-on-emerging-threats-and-capabilities-statement-for-the-re/",
        "filename": "_AARO_Director_SASC_Statement_202310.html",
        "title": "AARO Director Senate Testimony (Oct 2023)",
        "date": "2023-10-01",
        "type": "testimony",
        "save_as_html": True,
    },
]


def download(output_dir: str) -> dict:
    """Download Pentagon press releases and AARO briefings."""
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
            
            if doc.get("save_as_html"):
                local_path.write_text(resp.text)
            else:
                local_path.write_bytes(resp.content)
            
            print(f"✓ ({len(resp.content)} bytes)")
            results.append({"file": doc["filename"], "status": "downloaded", "size": len(resp.content)})
        except Exception as e:
            print(f"✗ {e}")
            results.append({"file": doc["filename"], "status": "error", "error": str(e)})
    
    # Write index
    with open(output_path / "_index.json", "w") as f:
        meta = {
            "source": "U.S. Department of Defense & AARO",
            "url": "https://www.defense.gov/",
            "notes": "Official UAP-related press releases, briefings, and AARO director statements.",
            "documents": DOCUMENTS,
            "results": results,
        }
        json.dump(meta, f, indent=2)
    
    return {"downloaded": sum(1 for r in results if r["status"] == "downloaded"), "total": len(DOCUMENTS)}

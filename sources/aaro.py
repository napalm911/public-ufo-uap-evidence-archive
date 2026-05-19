#!/usr/bin/env python3
"""
Source: AARO - All-domain Anomaly Resolution Office Reports
URL: https://www.aaro.mil/

The DoD office created to analyze UAP reports. Released Historical Record Report
in 2024 and various other documents.
"""

import json
from pathlib import Path

import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

# Known AARO documents and their alternate download locations
# (aaro.mil blocks direct access, so we use alternate gov sites)
FILES = [
    {
        "url": "https://media.defense.gov/2024/Mar/08/2003409233/-1/-1/0/EXECUTIVE-SUMMARY-OF-HRR-20240308.pdf",
        "filename": "AARO_Historical_Record_Report_Executive_Summary_20240308.pdf",
        "title": "AARO Historical Record Report - Executive Summary (March 2024)",
        "type": "report",
        "alternate_urls": [
            "https://www.documentcloud.org/documents/24453103-aaro-historical-record-report-exsum",
        ],
    },
    {
        "url": "https://media.defense.gov/2024/Mar/08/2003409232/-1/-1/0/UNCLASSIFIED-HRR-FULL-RELEASE-20240308.pdf",
        "filename": "AARO_Historical_Record_Report_Full_20240308.pdf",
        "title": "AARO Historical Record Report - Full (March 2024)",
        "type": "report",
    },
    {
        "url": "https://media.defense.gov/2024/Nov/14/2003586648/-1/-1/0/AARO-HRR-VOLUME-2.PDF",
        "filename": "AARO_Historical_Record_Report_Vol2_20241114.pdf",
        "title": "AARO Historical Record Report - Volume 2 (Nov 2024)",
        "type": "report",
    },
    {
        "url": "https://media.defense.gov/2022/May/18/2002999943/-1/-1/1/ESTABLISHMENT-OF-AARO.PDF",
        "filename": "AARO_Establishment_DoD_Directive_20220518.pdf",
        "title": "DoD Directive Establishing AARO (May 2022)",
        "type": "directive",
    },
    {
        "url": "https://media.defense.gov/2023/Sep/14/2003297036/-1/-1/0/AARO-MISSION-AND-ORGANIZATION-FACT-SHEET.PDF",
        "filename": "AARO_Mission_Org_Fact_Sheet_20230914.pdf",
        "title": "AARO Mission and Organization Fact Sheet (Sep 2023)",
        "type": "factsheet",
    },
]


def download(output_dir: str) -> dict:
    """Download AARO reports from defense.gov media server."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    results = []
    for file_info in FILES:
        local_path = output_path / file_info["filename"]
        
        if local_path.exists() and local_path.stat().st_size > 0:
            print(f"  ✓ {file_info['filename']} (already exists)")
            results.append({"file": file_info["filename"], "status": "exists"})
            continue
        
        # Try primary URL first
        success = False
        urls_to_try = [file_info["url"]] + file_info.get("alternate_urls", [])
        for url in urls_to_try:
            try:
                print(f"  Downloading {file_info['filename']}...", end=" ", flush=True)
                resp = requests.get(url, headers=HEADERS, timeout=60, allow_redirects=True)
                resp.raise_for_status()
                local_path.write_bytes(resp.content)
                print(f"✓ ({len(resp.content)} bytes)")
                results.append({
                    "file": file_info["filename"],
                    "status": "downloaded",
                    "size": len(resp.content),
                    "url_used": url,
                })
                success = True
                break
            except Exception as e:
                print(f"  {e}")
                continue
        
        if not success:
            print(f"  ✗ {file_info['filename']} - all URLs failed")
            results.append({"file": file_info["filename"], "status": "error"})
    
    # Write metadata
    with open(output_path / "_index.json", "w") as f:
        meta = {
            "source": "AARO - All-domain Anomaly Resolution Office (DoD)",
            "url": "https://www.aaro.mil/",
            "notes": "Created in 2022. Released Historical Record Report Mar 2024 and Nov 2024.",
            "files": FILES,
            "results": results,
        }
        json.dump(meta, f, indent=2)
    
    return {"downloaded": sum(1 for r in results if r["status"] == "downloaded"), "total": len(FILES)}

#!/usr/bin/env python3
"""
Source: NASA UAP Independent Study Team Report (2023-2024)
URL: https://science.nasa.gov/uap/

NASA's independent study on UAPs, including the 2023 team formation,
the public meetings, and the final 2024 report.
"""

import json
import os
import time
from pathlib import Path

import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

FILES = [
    {
        "url": "https://science.nasa.gov/wp-content/uploads/2023/09/uap-independent-study-team-report.pdf",
        "filename": "NASA_UAP_Independent_Study_Report_2023.pdf",
        "title": "NASA UAP Independent Study Team Report (Sep 2023)",
        "type": "report",
    },
    {
        "url": "https://www.nasa.gov/wp-content/uploads/2024/03/nasa-uap-response-v3.pdf",
        "filename": "NASA_UAP_Response_2024.pdf",
        "title": "NASA's UAP Research Response (Mar 2024)",
        "type": "response",
    },
    {
        "url": "https://www.nasa.gov/wp-content/uploads/2024/03/nasa-uap-director-announcement.pdf",
        "filename": "NASA_UAP_Director_Announcement_2024.pdf",
        "title": "NASA UAP Research Director Announcement (Mar 2024)",
        "type": "announcement",
    },
    {
        "url": "https://science.nasa.gov/uap/",
        "filename": "_nasa_uap_page.html",
        "title": "NASA UAP Page (archived)",
        "type": "webpage",
        "save_as_html": True,
    },
]


def download(output_dir: str) -> dict:
    """Download NASA UAP study documents."""
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
            resp = requests.get(file_info["url"], headers=HEADERS, timeout=60, allow_redirects=True)
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
    
    # Write metadata
    with open(output_path / "_index.json", "w") as f:
        meta = {
            "source": "NASA - UAP Independent Study Team",
            "url": "https://science.nasa.gov/uap/",
            "notes": "NASA convened an independent study team in 2022. Report released Sep 2023. UAP Research Director appointed Mar 2024.",
            "files": FILES,
            "results": results,
        }
        json.dump(meta, f, indent=2)
    
    return {"downloaded": sum(1 for r in results if r["status"] == "downloaded"), "total": len(FILES)}

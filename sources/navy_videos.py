#!/usr/bin/env python3
"""
Source: U.S. Navy UAP Videos (DoD-confirmed)
URL: https://www.defense.gov/News/Releases/Release/Article/2169488/

The three Navy videos declassified and released by the Department of Defense:
- FLIR1 (2004 - USS Nimitz incident)
- GIMBAL (2015 - USS Theodore Roosevelt)
- GOFAST (2015 - USS Theodore Roosevelt)

Officially designated 'Unidentified Aerial Phenomena' by DoD in 2020.
"""

import json
from pathlib import Path

import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

# These are the official DoD-released UAP videos
# Hosted on defense.gov media server
VIDEOS = [
    {
        "url": "https://media.defense.gov/2020/Apr/27/2002293156/-1/-1/0/FLIR1.MP4",
        "filename": "FLIR1_Nimitz_2004.mp4",
        "title": "FLIR1 - USS Nimitz Tic Tac Incident (2004)",
        "description": "Infrared footage of the Tic Tac UAP off the coast of San Diego. Recorded by F/A-18F FLIR pod.",
        "date": "2004-11-14",
        "type": "video",
    },
    {
        "url": "https://media.defense.gov/2020/Apr/27/2002293158/-1/-0/GIMBAL.MP4",
        "filename": "GIMBAL_USS_TR_2015.mp4",
        "title": "GIMBAL - USS Theodore Roosevelt (2015)",
        "description": "Footage of a UAP rotating against the wind off the east coast of Florida.",
        "date": "2015",
        "type": "video",
    },
    {
        "url": "https://media.defense.gov/2020/Apr/27/2002293157/-1/-0/GOFAST.MP4",
        "filename": "GOFAST_USS_TR_2015.mp4",
        "title": "GOFAST - USS Theodore Roosevelt (2015)",
        "description": "Footage showing a small object flying at high speed near the water surface.",
        "date": "2015",
        "type": "video",
    },
]


def download(output_dir: str) -> dict:
    """Download Navy UAP videos from defense.gov."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    results = []
    for video in VIDEOS:
        local_path = output_path / video["filename"]
        
        if local_path.exists() and local_path.stat().st_size > 0:
            print(f"  ✓ {video['filename']} (already exists, {local_path.stat().st_size} bytes)")
            results.append({"file": video["filename"], "status": "exists"})
            continue
        
        print(f"  Downloading {video['filename']} ({video['title']})...", end=" ", flush=True)
        try:
            # Use stream for large video files
            resp = requests.get(video["url"], headers=HEADERS, timeout=300, stream=True)
            resp.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"✓ ({local_path.stat().st_size} bytes)")
            results.append({"file": video["filename"], "status": "downloaded", "size": local_path.stat().st_size})
        except Exception as e:
            print(f"✗ {e}")
            results.append({"file": video["filename"], "status": "error", "error": str(e)})
    
    # Write metadata
    with open(output_path / "_index.json", "w") as f:
        meta = {
            "source": "U.S. Department of Defense",
            "notes": "Officially released by DoD on April 27, 2020. The videos had been circulating since 2007-2017, but DoD confirmed their authenticity and declassified them in 2020.",
            "videos": VIDEOS,
            "results": results,
        }
        json.dump(meta, f, indent=2)
    
    return {"downloaded": sum(1 for r in results if r["status"] == "downloaded"), "total": len(VIDEOS)}

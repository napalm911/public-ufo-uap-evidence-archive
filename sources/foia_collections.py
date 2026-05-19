#!/usr/bin/env python3
"""
Source: FOIA Collections Index (Black Vault & Major FOIA Archives)
URL: https://www.theblackvault.com/

The Black Vault is the largest non-governmental FOIA archive of UFO/UAP documents,
containing over 100,000 pages from CIA, FBI, DIA, NSA, and other agencies.
"""

import json
from pathlib import Path

import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

# Major FOIA UFO collections indexed here
# The Black Vault requires membership for bulk download, so we document
# the collection and provide links to key free sources.
FOIA_SOURCES = [
    {
        "name": "The Black Vault - Government UFO Documents",
        "url": "https://www.theblackvault.com/document-category/government-ufo-documents/",
        "description": "Largest FOIA UFO document archive. Over 100,000 pages from CIA, FBI, DIA, NSA, USAF, USN, DoD, DOE.",
        "type": "foia_archive",
        "access_notes": "Some documents require free membership for download. API available for bulk access.",
    },
    {
        "name": "National Security Archive - UFO Collection (GWU)",
        "url": "https://nsarchive.gwu.edu/project/ufo-project",
        "description": "George Washington University's National Security Archive has a dedicated UFO collection from FOIA requests.",
        "type": "academic_archive",
        "access_notes": "Free access. Many documents available directly on website.",
    },
    {
        "name": "NNSA FOIA Reading Room",
        "url": "https://www.energy.gov/nnsa/nnsa-foia-reading-room",
        "description": "Department of Energy / NNSA FOIA documents including records of UFO incidents near nuclear facilities.",
        "type": "government_foia",
        "access_notes": "Includes Malmstrom AFB incident, nuclear base UAP sightings.",
    },
    {
        "name": "DIA FOIA Reading Room",
        "url": "https://www.dia.mil/FOIA/FOIA-Electronic-Reading-Room/",
        "description": "Defense Intelligence Agency FOIA documents, including Advanced Aerospace Threat Identification Program (AATIP) records.",
        "type": "government_foia",
        "access_notes": "Search for 'AATIP', 'UAP', 'Advanced Aerospace'.",
    },
    {
        "name": "NSA UFO Documents (via GovernmentAttic)",
        "url": "https://www.governmentattic.org/ufo.html",
        "description": "National Security Agency declassified UFO documents obtained via FOIA.",
        "type": "foia_archive",
        "access_notes": "Free download. Hundreds of NSA documents.",
    },
    {
        "name": "CIA Reading Room - UFO Search",
        "url": "https://www.cia.gov/readingroom/search/site/ufo",
        "description": "Search the CIA's CREST database for UFO-related records. 500+ results.",
        "type": "government_foia",
        "access_notes": "Free search and download. Rate limited.",
    },
]


def download(output_dir: str) -> dict:
    """Create the FOIA archive index."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Write the FOIA sources index
    with open(output_path / "_index.json", "w") as f:
        meta = {
            "source": "FOIA Collections - Major Archives",
            "notes": "Index of major FOIA archives containing UFO/UAP documents. Each source has its own download mechanism.",
            "sources": FOIA_SOURCES,
        }
        json.dump(meta, f, indent=2)
    
    print(f"  Indexed {len(FOIA_SOURCES)} FOIA collection sources")
    return {"sources_indexed": len(FOIA_SOURCES)}

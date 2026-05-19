#!/usr/bin/env python3
"""
Source: Foreign Government UAP Releases
URLs: Various (UK Ministry of Defence, French COMETA, etc.)

Supplementary UAP/UFO documents released by foreign governments:
UK, France, Belgium, Brazil, Chile, Japan, and others.
"""

import json
from pathlib import Path

import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

FOREIGN_SOURCES = [
    {
        "name": "UK Ministry of Defence - UFO Files",
        "url": "https://www.nationalarchives.gov.uk/ufos/",
        "description": "UK MoD declassified UFO files released via The National Archives. Thousands of pages covering 1950-2009.",
        "type": "government",
        "country": "UK",
    },
    {
        "name": "France - COMETA Report (1999)",
        "url": "https://www.ufoevidence.org/documents/doc1689.htm",
        "description": "French COMETA Report - study by the Institute of Advanced Studies for National Defence. Concluded UFOs are real and likely extraterrestrial.",
        "type": "government_study",
        "country": "France",
    },
    {
        "name": "France - GEIPAN (CNES)",
        "url": "https://www.cnes-geipan.fr/",
        "description": "French government's official UAP investigation unit. Publishes case reports and statistics.",
        "type": "government_agency",
        "country": "France",
    },
    {
        "name": "Brazil - Brazilian Air Force UFO Files",
        "url": "https://www.ufo.com.br/",
        "description": "Brazilian Air Force declassified UFO investigation documents. Notably the 1986 Varginha incident files.",
        "type": "government",
        "country": "Brazil",
    },
    {
        "name": "Chile - CEFAA (Civil Aviation)",
        "url": "https://www.dgac.gob.cl/cefaa/",
        "description": "Chilean government's Committee for the Study of Anomalous Aerial Phenomena.",
        "type": "government_agency",
        "country": "Chile",
    },
    {
        "name": "Japan - Ministry of Defense UAP Policy",
        "url": "https://www.mod.go.jp/j/approach/defense/others/ufo/",
        "description": "Japan's MoD established official UAP reporting procedures in 2020.",
        "type": "government_policy",
        "country": "Japan",
    },
    {
        "name": "Canada - Transport Canada UFO Files",
        "url": "https://www.collectionscanada.gc.ca/ufo/index-e.html",
        "description": "Transport Canada and Canadian government UFO investigation files (1950-1990s).",
        "type": "government",
        "country": "Canada",
    },
    {
        "name": "Uruguay - Uruguayan Air Force UFO Division",
        "url": "https://www.gub.uy/fuerza-aerea/comision-recepcion-analisis-informes-ovni",
        "description": "Uruguayan Air Force maintains an official UFO investigation commission.",
        "type": "government",
        "country": "Uruguay",
    },
    {
        "name": "Belgium - SOBEPS / Belgian UFO Wave (1989-1991)",
        "url": "https://www.sbep.be/",
        "description": "Belgian government and air force investigation of the 1989-1991 UFO wave. Includes F-16 intercept radar data.",
        "type": "government_collaboration",
        "country": "Belgium",
    },
]


def download(output_dir: str) -> dict:
    """Create the foreign government releases index."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    with open(output_path / "_index.json", "w") as f:
        meta = {
            "source": "Foreign Government UAP Releases",
            "notes": "Supplementary sources from governments outside the United States that have officially released UFO/UAP documents.",
            "sources": FOREIGN_SOURCES,
        }
        json.dump(meta, f, indent=2)
    
    print(f"  Indexed {len(FOREIGN_SOURCES)} foreign government sources")
    return {"sources_indexed": len(FOREIGN_SOURCES)}

#!/usr/bin/env python3
"""
Generate metadata indexes for AI analysis.
Creates:
- master_index.json (all sources, file counts, types)
- timeline.json (chronological ordering of documents)
- topic_tags.json (topic-tagged document map)
- source_index.json (per-source summary)

Usage:
    python scripts/generate_metadata.py
"""

import json
import re
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
METADATA_DIR = BASE_DIR / "metadata"


def scan_all_files() -> dict:
    """Walk the data directory and catalog every file."""
    catalog = {"by_source": {}, "all_files": []}
    
    for source_dir in sorted(DATA_DIR.iterdir()):
        if not source_dir.is_dir() or source_dir.name.startswith("."):
            continue
        
        source_key = source_dir.name
        files = []
        
        for f in source_dir.rglob("*"):
            if not f.is_file() or f.name in (".gitkeep", "_index.json", "_summary.json"):
                continue
            
            stat = f.stat()
            entry = {
                "path": str(f.relative_to(BASE_DIR)),
                "filename": f.name,
                "extension": f.suffix.lower() or "no_ext",
                "size_bytes": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "source": source_key,
            }
            files.append(entry)
            catalog["all_files"].append(entry)
        
        catalog["by_source"][source_key] = {
            "file_count": len(files),
            "total_size_bytes": sum(f["size_bytes"] for f in files),
            "extensions": {},
        }
        for f in files:
            ext = f["extension"]
            catalog["by_source"][source_key]["extensions"][ext] = \
                catalog["by_source"][source_key]["extensions"].get(ext, 0) + 1
    
    return catalog


def build_timeline(catalog: dict) -> list:
    """Extract date information from filenames and build a timeline."""
    timeline = []
    date_patterns = [
        r"(\d{4})[-/](\d{2})[-/](\d{2})",  # 2023-07-26
        r"(\d{4})(\d{2})(\d{2})",           # 20230726
        r"(\d{4})[-_](\d{2})",              # 2023-07
        r"(\d{4})",                          # 2023
    ]
    
    for f in catalog["all_files"]:
        date_found = None
        for pattern in date_patterns:
            match = re.search(pattern, f["filename"])
            if match:
                groups = match.groups()
                if len(groups) == 3 and len(groups[0]) == 4:
                    date_found = f"{groups[0]}-{groups[1]}-{groups[2]}"
                elif len(groups) == 2:
                    date_found = f"{groups[0]}-{groups[1]}"
                elif len(groups) == 1:
                    date_found = groups[0]
                break
        
        # Check _index.json for date field
        if date_found:
            timeline.append({
                "date": date_found,
                "file": f["path"],
                "source": f["source"],
            })
    
    timeline.sort(key=lambda x: x["date"])
    return timeline


def build_topic_tags(catalog: dict) -> dict:
    """Build topic-tagged document map based on filename keywords."""
    topics = {
        "hearing": ["hearing", "testimony", "transcript", "statement"],
        "virginia_incidents": ["nimitz", "tic tac", "flir", "2004"],
        "roosevelt_incidents": ["gimbal", "gofast", "roosevelt", "uss tr"],
        "disclosure_legislation": ["disclosure act", "ndaa", "schumer", "rounds", "legislation"],
        "nuclear_connections": ["nnsa", "doe", "nuclear", "weapon", "malmstrom"],
        "project_blue_book": ["blue book", "project blue", "usaf"],
        "cia_documents": ["cia", "crest", "osd", "stargate"],
        "fbi_documents": ["fbi", "hottel"],
        "aaro_reports": ["aaro", "historical record"],
        "nasa_study": ["nasa", "independent study"],
        "international": ["uk", "france", "brazil", "chile", "japan"],
    }
    
    tag_map = {}
    for f in catalog["all_files"]:
        name_lower = f["filename"].lower()
        matched_topics = []
        
        for topic, keywords in topics.items():
            for kw in keywords:
                if kw.lower() in name_lower:
                    matched_topics.append(topic)
                    break
        
        if matched_topics:
            tag_map[f["path"]] = matched_topics
    
    return tag_map


def main():
    print("Generating metadata indexes...")
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Scan all files
    catalog = scan_all_files()
    print(f"  Found {len(catalog['all_files'])} files across {len(catalog['by_source'])} sources")
    
    # 1. Source index
    source_index = {}
    for source_key, info in catalog["by_source"].items():
        source_index[source_key] = {
            "file_count": info["file_count"],
            "total_size_bytes": info["total_size_bytes"],
            "total_size_mb": round(info["total_size_bytes"] / (1024 * 1024), 2),
            "file_types": info["extensions"],
        }
    
    with open(METADATA_DIR / "source_index.json", "w") as f:
        json.dump(source_index, f, indent=2)
    print("  ✓ source_index.json")
    
    # 2. Master index
    master = {
        "generated": datetime.now().isoformat(),
        "total_files": len(catalog["all_files"]),
        "total_sources": len(catalog["by_source"]),
        "sources": source_index,
    }
    with open(METADATA_DIR / "master_index.json", "w") as f:
        json.dump(master, f, indent=2)
    print("  ✓ master_index.json")
    
    # 3. Timeline
    timeline = build_timeline(catalog)
    timeline_meta = {
        "total_dated_entries": len(timeline),
        "entries": timeline,
    }
    with open(METADATA_DIR / "timeline.json", "w") as f:
        json.dump(timeline_meta, f, indent=2)
    print(f"  ✓ timeline.json ({len(timeline)} dated entries)")
    
    # 4. Topic tags
    tag_map = build_topic_tags(catalog)
    with open(METADATA_DIR / "topic_tags.json", "w") as f:
        json.dump(tag_map, f, indent=2)
    print(f"  ✓ topic_tags.json ({len(tag_map)} tagged files)")
    
    print("\n✓ Metadata generation complete!")


if __name__ == "__main__":
    main()

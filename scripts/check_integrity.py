#!/usr/bin/env python3
"""
Check the integrity of downloaded files.
Verifies file sizes match expectations and identifies corrupted files.

Usage:
    python scripts/check_integrity.py
    python scripts/check_integrity.py --source aaro
"""

import argparse
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def check_source(source_dir: Path) -> dict:
    """Check all files in a source directory."""
    pdfs = list(source_dir.rglob("*.pdf"))
    mp4s = list(source_dir.rglob("*.mp4"))
    htmls = list(source_dir.rglob("*.html"))
    
    results = {"ok": 0, "empty": 0, "small": 0, "warnings": [], "files": []}
    
    for f in pdfs + mp4s + htmls:
        if f.name.startswith("_"):
            continue
        
        size = f.stat().st_size
        ext = f.suffix.lower()
        
        entry = {
            "path": str(f.relative_to(BASE_DIR)),
            "size": size,
            "ext": ext,
        }
        
        if size == 0:
            entry["status"] = "empty"
            results["empty"] += 1
        elif ext == ".pdf" and size < 1024:
            entry["status"] = "too_small"
            results["small"] += 1
            results["warnings"].append(f"  ⚠ Likely corrupted: {f.name} ({size} bytes)")
        elif ext == ".mp4" and size < 10240:
            entry["status"] = "too_small"
            results["small"] += 1
            results["warnings"].append(f"  ⚠ Too small for video: {f.name} ({size} bytes)")
        else:
            entry["status"] = "ok"
            results["ok"] += 1
        
        results["files"].append(entry)
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Check downloaded file integrity")
    parser.add_argument("--source", "-s", help="Specific source to check")
    args = parser.parse_args()
    
    print("\nChecking file integrity...")
    print("-" * 50)
    
    if args.source:
        src_dir = DATA_DIR / args.source.replace("-", "_")
        if not src_dir.exists():
            print(f"Source not found: {src_dir}")
            return
        results = {src_dir.name: check_source(src_dir)}
    else:
        results = {}
        for source_dir in sorted(DATA_DIR.iterdir()):
            if source_dir.is_dir() and not source_dir.name.startswith("."):
                results[source_dir.name] = check_source(source_dir)
    
    total_ok = sum(r["ok"] for r in results.values())
    total_empty = sum(r["empty"] for r in results.values())
    total_small = sum(r["small"] for r in results.values())
    
    for source_name, result in results.items():
        status = "✓" if result["empty"] == 0 and result["small"] == 0 else "⚠"
        print(f"  {status} {source_name}: {result['ok']} ok, {result['empty']} empty, {result['small']} small")
        for w in result["warnings"]:
            print(w)
    
    print("-" * 50)
    print(f"Total: {total_ok} ok, {total_empty} empty, {total_small} suspicious")
    
    if total_empty == 0 and total_small == 0:
        print("\n✓ All files look good!")
    else:
        print(f"\n⚠ {total_empty + total_small} files need attention")
    
    # Write report
    report = {
        "checked": len(results),
        "ok": total_ok,
        "empty": total_empty,
        "suspicious": total_small,
        "sources": {
            k: {"ok": v["ok"], "empty": v["empty"], "small": v["small"]}
            for k, v in results.items()
        }
    }
    report_path = BASE_DIR / "metadata" / "integrity_check.json"
    BASE_DIR.joinpath("metadata").mkdir(exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"  Report: {report_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Extract text from downloaded PDFs for AI analysis.
Converts PDF content to plaintext for vector search, LLM context, and training data.

Usage:
    python scripts/extract_text.py                  # Extract all PDFs
    python scripts/extract_text.py --source aaro    # Specific source
    python scripts/extract_text.py --output custom_output_dir
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF required. Install: pip install PyMuPDF")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def extract_pdf(pdf_path: Path, output_path: Path) -> dict:
    """Extract text from a single PDF and save as .txt."""
    try:
        doc = fitz.open(pdf_path)
        text_parts = []
        page_count = len(doc)
        for page_num, page in enumerate(doc):
            text = page.get_text()
            if text.strip():
                text_parts.append(f"--- Page {page_num + 1} ---\n{text}")
        doc.close()
        
        full_text = "\n\n".join(text_parts)
        output_file = output_path / f"{pdf_path.stem}.txt"
        output_file.write_text(full_text, encoding="utf-8")
        
        return {
            "file": pdf_path.name,
            "pages": page_count,
            "chars": len(full_text),
            "output": str(output_file.relative_to(BASE_DIR)),
            "status": "ok",
        }
    except Exception as e:
        return {
            "file": pdf_path.name,
            "status": "error",
            "error": str(e),
        }


def extract_source(source_dir: Path, output_base: Path) -> list:
    """Extract all PDFs in a source directory."""
    pdfs = list(source_dir.rglob("*.pdf"))
    if not pdfs:
        return []
    
    # Create parallel output structure
    rel_path = source_dir.relative_to(DATA_DIR)
    output_dir = output_base / rel_path
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = []
    for pdf_path in pdfs:
        result = extract_pdf(pdf_path, output_dir)
        results.append(result)
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Extract text from downloaded UAP PDFs")
    parser.add_argument("--source", "-s", help="Specific source subdirectory to process")
    parser.add_argument("--output", "-o", default=str(BASE_DIR / "analysis" / "extracted_text"),
                      help="Output directory for extracted text")
    args = parser.parse_args()
    
    output_base = Path(args.output)
    output_base.mkdir(parents=True, exist_ok=True)
    
    if args.source:
        src_dir = DATA_DIR / args.source.replace("-", "_")
        if not src_dir.exists():
            print(f"Source directory not found: {src_dir}")
            sys.exit(1)
        results = extract_source(src_dir, output_base)
    else:
        results = []
        for source_dir in sorted(DATA_DIR.iterdir()):
            if source_dir.is_dir() and not source_dir.name.startswith("."):
                src_results = extract_source(source_dir, output_base)
                results.extend(src_results)
                print(f"  {source_dir.name}: {len(src_results)} files extracted")
    
    # Write extraction report
    report_path = output_base / "_extraction_report.json"
    successful = [r for r in results if r["status"] == "ok"]
    failed = [r for r in results if r["status"] == "error"]
    
    report = {
        "total_processed": len(results),
        "successful": len(successful),
        "failed": len(failed),
        "total_chars": sum(r.get("chars", 0) for r in successful),
        "results": results,
    }
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✓ Extraction complete")
    print(f"  Processed: {len(results)} files")
    print(f"  Successful: {len(successful)}")
    print(f"  Failed: {len(failed)}")
    print(f"  Total chars extracted: {report['total_chars']:,}")
    print(f"  Report: {report_path}")


if __name__ == "__main__":
    main()

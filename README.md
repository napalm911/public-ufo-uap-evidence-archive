# Public UFO / UAP Government Evidence Archive

> **Curated repository of declassified, FOIA-released, and publicly available U.S. government documents related to Unidentified Flying Objects (UFOs) and Unidentified Anomalous Phenomena (UAPs).**

**Purpose:** Provide a machine-readable, AI-analysis-ready archive of all U.S. government-released UFO/UAP evidence — documents, briefings, videos, reports, and metadata — organized by source for research, analysis, and content creation.

**Self-contained:** This repo downloads everything locally. No external dependencies for the raw data once fetched.

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/napalm911/public-ufo-uap-evidence-archive.git
cd public-ufo-uap-evidence-archive

# Install dependencies
pip install -r requirements.txt

# Run the full downloader (will take a while - thousands of files)
python download-all.py

# Or download a specific source
python download-all.py --source fbi
python download-all.py --source cia-crest
python download-all.py --source aaro
```

---

## Sources Included

| # | Source | Type | Est. Docs | Status |
|---|--------|------|-----------|--------|
| 1 | **FBI Vault - UFO Files** | Declassified FBI records | ~2,000 pages | ✅ |
| 2 | **CIA CREST Archive (UFO-related)** | Declassified CIA docs (25yr program) | ~500+ docs | ✅ |
| 3 | **National Archives - Project Blue Book** | USAF investigation (1947-1969) | ~12,000+ reports | ✅ |
| 4 | **ODNI UAP Preliminary Assessment (2021)** | Official intelligence assessment | 1 report | ✅ |
| 5 | **AARO Historical Record Reports (2024)** | DoD UAP office reports | 2 reports + supplements | ✅ |
| 6 | **NASA UAP Independent Study Report** | NASA study & findings | 1 report + briefings | ✅ |
| 7 | **U.S. Navy UAP Videos (DoD-confirmed)** | Declassified military footage | 3 videos | ✅ |
| 8 | **Pentagon AARO Briefings & Testimony** | Congressional testimony & press briefs | ~20 transcripts | ✅ |
| 9 | **UAP Disclosure Act (NDAA) Language** | Legislation text | 5 law docs | ✅ |
| 10 | **FOIA Collections (Black Vault index)** | Community FOIA archive index | 100,000+ pages indexed | ✅ |
| 11 | **Department of Energy / NNSA Docs** | Nuclear security UFO docs | ~100 docs | ✅ |
| 12 | **Congressional Hearings & Testimony** | UAP hearing transcripts (2022-2025) | ~15 transcripts | ✅ |
| 13 | **Foreign Gov Releases (supplementary)** | UK, France, other releases | ~500 docs | ✅ |

## Directory Structure

```
public-ufo-uap-evidence-archive/
├── README.md                           # This file
├── download-all.py                     # Main downloader script
├── requirements.txt                    # Python deps
├── sources/                            # Per-source downloaders
│   ├── fbi_vault.py                   # FBI vault crawler
│   ├── cia_crest.py                   # CIA CREST archive crawler
│   ├── project_blue_book.py           # Project Blue Book
│   ├── odni_report.py                 # ODNI assessment
│   ├── aaro.py                        # AARO reports
│   ├── nasa_uap.py                    # NASA UAP study
│   ├── navy_videos.py                 # Navy UAP videos
│   ├── pentagon_briefings.py          # Pentagon transcripts
│   ├── disclosure_act.py              # Legislation
│   ├── foia_collections.py            # FOIA archive index
│   ├── doe_nnsa.py                    # DOE/NNSA docs
│   ├── congressional_hearings.py      # Hearing transcripts
│   └── foreign_releases.py            # Foreign gov releases
├── data/                              # Downloaded data (gitignored)
│   ├── fbi_vault/                    # FBI UFO files
│   ├── cia_crest/                    # CIA UFO-related docs
│   ├── project_blue_book/            # Blue Book files
│   ├── odni_report/                  # ODNI report PDF
│   ├── aaro/                         # AARO reports
│   ├── nasa_uap/                     # NASA study
│   ├── navy_videos/                  # Navy footage
│   ├── pentagon_briefings/           # Transcripts
│   ├── disclosure_act/              # Law documents
│   ├── foia_collections/            # FOIA archive index
│   ├── doe_nnsa/                    # DOE docs
│   ├── congressional_hearings/      # Hearing transcripts
│   └── foreign_releases/            # Foreign docs
├── metadata/                          # Indexes & metadata for AI
│   ├── master_index.json             # Combined metadata index
│   ├── source_index.json             # Per-source summary
│   ├── timeline.json                 # Chronological index
│   └── topic_tags.json              # Topic-tagged document map
├── analysis/                          # AI analysis outputs (user fills)
│   ├── notebooks/                    # Example analysis notebooks
│   └── reports/                      # Generated analysis reports
└── scripts/                          # Utility scripts
    ├── check_integrity.py            # Verify downloaded files
    ├── generate_metadata.py          # Regenerate metadata index
    └── extract_text.py               # OCR/PDF text extraction
```

## For AI Analysis

Once downloaded, you can:

1. **Vector search:** Load all PDFs/text into a vector DB for semantic search
2. **Cross-reference:** Correlate witness names, locations, dates across sources
3. **Timeline analysis:** Map document chronology (use `metadata/timeline.json`)
4. **Content extraction:** Run `scripts/extract_text.py` to extract plaintext from all PDFs
5. **Training data:** Convert document extracts to fine-tuning format

Example Claude / GPT prompt:
> "Using the documents in data/aaro/, data/odni_report/, and data/pentagon_briefings/, analyze the official U.S. government position on UAPs from 2021-2025, comparing the language in the ODNI Preliminary Assessment vs. the AARO Historical Record Report."

## Notes on What Trump Permitted / Signed

- **Dec 2020:** Trump signed the **Intelligence Authorization Act for FY2021**, which included a provision requiring the ODNI to deliver a report on UAPs to Congress within 180 days. This led to the landmark June 2021 ODNI Preliminary Assessment.
- **Trump's UAP comments:** Trump has stated in multiple interviews (OANN, Fox News) that he was "briefed" on UAPs, said the subject is "very interesting," and that he'd "declassify" more if asked — but no specific bulk declassification action occurred during his presidency beyond signing the NDAA provision.
- **The real disclosure wave (2021-2025)** happened under Biden — but **Trump's 2020 NDAA signing** is the legislative trigger that started the modern UAP disclosure cycle.

## License

All documents in this repository are public domain (U.S. government works) or used under fair use / FOIA. The scripts and metadata are MIT.

**This repo does not host copyrighted content — it downloads publicly available government documents from official sources.**

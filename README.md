# Public UFO / UAP Government Evidence Archive

> **Curated repository of declassified, FOIA-released, and publicly available U.S. government documents related to Unidentified Flying Objects (UFOs) and Unidentified Anomalous Phenomena (UAPs).**

**Purpose:** Provide a machine-readable, AI-analysis-ready archive of all U.S. government-released UFO/UAP evidence — documents, briefings, videos, reports, and metadata — organized by source for research, analysis, and content creation.

Includes a **branded web app** with semantic vector search and RAG chat powered by DeepSeek.

---

## Quick Start (End-to-End)

**Prerequisites:** Python 3.10+, Node.js 18+, network access for downloads, [DeepSeek API key](https://platform.deepseek.com/) for chat.

```bash
git clone https://github.com/napalm911/public-ufo-uap-evidence-archive.git
cd public-ufo-uap-evidence-archive

# Configure API key
cp example.env .env
# Edit .env and set DEEPSEEK_API_KEY=your_key_here

# Full pipeline: setup → download → metadata → extract → index → build frontend
make all

# Start the website
make dev
# Open http://localhost:8000
```

### Makefile Targets

| Target | Description |
|--------|-------------|
| `make setup` | Create venv, install Python + Node deps, copy `.env` |
| `make download` | Download all 13 document sources |
| `make metadata` | Generate JSON indexes (timeline, topics, etc.) |
| `make extract` | Extract plaintext from PDFs |
| `make index` | Build ChromaDB vector index |
| `make check` | Verify downloaded file integrity |
| `make pipeline` | Run download → metadata → extract → index → check |
| `make all` | setup + pipeline + build (full E2E) |
| `make build` | Build frontend static assets |
| `make dev` | Run API + serve built frontend on `:8000` |
| `make dev-split` | API on `:8000` + Vite dev server on `:5173` |
| `make test` | Run pytest suite (offline) |
| `make demo` | Index fixture text for quick testing without download |
| `make clean` | Remove venv, node_modules, vector store, caches |

---

## Web App

The archive includes a **browse-first** research website:

| Route | Purpose |
|-------|---------|
| `/` | Archive home — source cards, stats, links to Timeline & Topics |
| `/sources/:key` | File list for a government source |
| `/documents/:id` | Document detail — metadata, text preview, download |
| `/timeline` | Chronological browse by date |
| `/topics` | Thematic browse (hearings, AARO, legislation, etc.) |
| `/ask` | RAG chat with DeepSeek (grounded in retrieved excerpts) |
| `/search` | Semantic search over indexed text |

**Navigation:** persistent sidebar (desktop) or bottom tabs (mobile). Every source, file, timeline entry, and topic is clickable. Citations in chat/search link to document pages.

**Browse API:** `GET /api/documents`, `GET /api/timeline`, `GET /api/topics`, `GET /files/...` for original downloads.

### Environment Variables

Copy [`example.env`](example.env) to `.env`:

| Variable | Description |
|----------|-------------|
| `DEEPSEEK_API_KEY` | Required for chat (get from DeepSeek) |
| `DEEPSEEK_BASE_URL` | Default: `https://api.deepseek.com` |
| `DEEPSEEK_MODEL` | Default: `deepseek-v4-flash` |
| `EMBEDDING_PROVIDER` | `local` (default) or `openai` |
| `EMBEDDING_MODEL` | Default: `all-MiniLM-L6-v2` |
| `CHROMA_PATH` | Vector store location (default: `./data/vector_store`) |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | Text chunking for indexing |
| `TOP_K` | Number of chunks retrieved per query |
| `HOST` / `PORT` | Server bind address |

Embeddings run locally by default (no extra API key). DeepSeek handles chat generation only.

---

## Manual CLI Usage

```bash
# Install dependencies only
make setup

# Download specific source
.venv/bin/python download-all.py --source fbi
.venv/bin/python download-all.py --list

# Regenerate metadata
.venv/bin/python scripts/generate_metadata.py

# Extract PDF text
.venv/bin/python scripts/extract_text.py

# Build vector index
.venv/bin/python scripts/build_index.py --force
```

---

## Sources Included

| # | Source | CLI key | Data dir |
|---|--------|---------|----------|
| 1 | FBI Vault - UFO Files | `fbi` | `data/fbi/` |
| 2 | CIA CREST Archive | `cia-crest` | `data/cia_crest/` |
| 3 | Project Blue Book | `blue-book` | `data/blue_book/` |
| 4 | ODNI UAP Assessment (2021) | `odni` | `data/odni/` |
| 5 | AARO Historical Record Reports | `aaro` | `data/aaro/` |
| 6 | NASA UAP Independent Study | `nasa` | `data/nasa/` |
| 7 | U.S. Navy UAP Videos | `navy-videos` | `data/navy_videos/` |
| 8 | Pentagon AARO Briefings | `pentagon` | `data/pentagon/` |
| 9 | UAP Disclosure Act / NDAA | `disclosure-act` | `data/disclosure_act/` |
| 10 | FOIA Collections Index | `foia` | `data/foia/` |
| 11 | DOE / NNSA Documents | `doe` | `data/doe/` |
| 12 | Congressional Hearings | `congress` | `data/congress/` |
| 13 | Foreign Government Releases | `foreign` | `data/foreign/` |

---

## Directory Structure

```
public-ufo-uap-evidence-archive/
├── Makefile                    # End-to-end workflow
├── example.env                 # Environment template
├── download-all.py             # Main downloader
├── requirements.txt            # Core Python deps
├── requirements-web.txt        # API + vector search deps
├── requirements-dev.txt        # Test deps
├── api/                        # FastAPI backend (RAG + search)
├── frontend/                   # React web app
├── sources/                    # Per-source downloaders
├── data/                       # Downloaded files (gitignored)
├── metadata/                   # JSON indexes
├── analysis/
│   ├── extracted_text/         # PDF plaintext
│   └── notebooks/              # Jupyter examples
├── scripts/
│   ├── generate_metadata.py
│   ├── extract_text.py
│   ├── build_index.py          # Vector indexing
│   └── check_integrity.py
└── tests/                      # Pytest suite
```

---

## For AI Analysis

Once downloaded and indexed:

1. **Vector search:** Semantic search via the web app or `POST /api/search`
2. **RAG chat:** Ask questions via the web app or `POST /api/chat`
3. **Cross-reference:** Use `metadata/timeline.json` and `metadata/topic_tags.json`
4. **Notebooks:** See `analysis/notebooks/01_basic_analysis.ipynb`

Example prompt:
> "Using documents from data/aaro/, data/odni/, and data/pentagon/, analyze the official U.S. government position on UAPs from 2021-2025."

---

## Notes on What Trump Permitted / Signed

- **Dec 2020:** Trump signed the **Intelligence Authorization Act for FY2021**, which included a provision requiring the ODNI to deliver a report on UAPs to Congress within 180 days. This led to the landmark June 2021 ODNI Preliminary Assessment.
- **Trump's UAP comments:** Trump has stated in multiple interviews (OANN, Fox News) that he was "briefed" on UAPs, said the subject is "very interesting," and that he'd "declassify" more if asked — but no specific bulk declassification action occurred during his presidency beyond signing the NDAA provision.
- **The real disclosure wave (2021-2025)** happened under Biden — but **Trump's 2020 NDAA signing** is the legislative trigger that started the modern UAP disclosure cycle.

---

## License

All documents in this repository are public domain (U.S. government works) or used under fair use / FOIA. The scripts and metadata are MIT.

**This repo does not host copyrighted content — it downloads publicly available government documents from official sources.**

.PHONY: setup download metadata extract index check pipeline all build dev dev-split test demo clean

PYTHON ?= python3
VENV := .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python
NPM := npm

setup:
	@echo "==> Setting up Python virtual environment..."
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt -r requirements-web.txt -r requirements-dev.txt
	@echo "==> Installing frontend dependencies..."
	@cd frontend && $(NPM) install
	@if [ ! -f .env ]; then cp example.env .env && echo "Created .env from example.env — add your DEEPSEEK_API_KEY"; fi
	@mkdir -p data analysis/extracted_text
	@echo "✓ Setup complete"

download:
	$(PY) download-all.py

metadata:
	$(PY) scripts/generate_metadata.py

extract:
	$(PY) scripts/extract_text.py

index:
	$(PY) scripts/build_index.py

check:
	$(PY) scripts/check_integrity.py

pipeline: download metadata extract index check
	@echo "✓ Pipeline complete"

build:
	@cd frontend && $(NPM) run build

all: setup pipeline build
	@echo "✓ Full end-to-end setup complete. Run 'make dev' to start the website."

dev:
	$(PY) -m uvicorn api.main:app --host $$(grep -E '^HOST=' .env 2>/dev/null | cut -d= -f2- || echo 0.0.0.0) --port $$(grep -E '^PORT=' .env 2>/dev/null | cut -d= -f2- || echo 8000) --reload

dev-split:
	@echo "Starting API on :8000 and Vite on :5173..."
	@$(PY) -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload & \
	cd frontend && $(NPM) run dev

test:
	$(PY) -m pytest tests/ -v

demo:
	@mkdir -p analysis/extracted_text/demo
	@cp tests/fixtures/extracted_text/demo/*.txt analysis/extracted_text/demo/
	$(PY) scripts/build_index.py --text-dir analysis/extracted_text/demo --force
	@echo "✓ Demo index built from fixtures"

clean:
	rm -rf $(VENV) frontend/node_modules frontend/dist data/vector_store .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

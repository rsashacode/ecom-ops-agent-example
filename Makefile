.PHONY: api ui test fmt lint up down data ingest index

python := uv run

api:
	$(python) uvicorn apps.api.main:app --reload --port 8000

ui:
	$(python) streamlit run apps/ui/home.py --server.port 8501

test:
	$(python) pytest -q

fmt:
	$(python) black .
	$(python) ruff check --fix .

lint:
	$(python) ruff check .
	$(python) mypy apps agent pipelines

data:
	@echo "placeholder: will download data later"

ingest:
	$(python) python pipelines/ingest.py

index:
	$(python) python pipelines/build_index.py

up:
	docker compose -f infra/docker-compose.yml up -d

down:
	docker compose -f infra/docker-compose.yml down

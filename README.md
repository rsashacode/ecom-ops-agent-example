# ecom-ops-agent-example
A multi-agent assistant that answers customer inquiries, proposes refund/return decisions, and explains its reasoning using both structured order data (SQL) and unstructured policy docs (RAG)

```bash
uv venv && source .venv/bin/activate
uv sync
make api   # http://localhost:8000/health
make ui    # http://localhost:8501
make test
```

- `make api` serves FastAPI on `:8000` and `/health` returns `ok`
- `make ui` opens Streamlit, posts to `/v1/chat`, and displays the echo
- `make test` or `uv run pytest` for tests
- `make fmt` run black and ruff checks with fix
- `make lint` ruff and mypy checks
- `make up` or `docker compose up` builds and runs containers
- `make down` or `docker compose down` stops containers

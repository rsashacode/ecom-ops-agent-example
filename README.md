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
- `uv run pytest` for tests
- `pre-commit` is installed and fixes style on commit
- `docker compose up` builds and runs the API + UI containers

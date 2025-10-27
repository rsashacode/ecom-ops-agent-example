from fastapi import FastAPI

from .routers import agents

app = FastAPI(title="E-Com Ops Agent API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(agents.router, prefix="/v1")

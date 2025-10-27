from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["agents"])


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(req: ChatRequest):
    return {"reply": f"Echo: {req.message}", "tools_used": []}

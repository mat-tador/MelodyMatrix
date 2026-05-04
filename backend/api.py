from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any

from backend.chatbot import get_chat_result

app = FastAPI()


class ChatRequest(BaseModel):
    message: str
    dashboard_state: Optional[Dict[str, Any]] = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(req: ChatRequest):
    result = get_chat_result(req.message, req.dashboard_state)
    return result
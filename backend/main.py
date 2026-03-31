from typing import Optional, Dict, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from chatbot import get_chat_result

app = FastAPI(title="Melody Matrix AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    dashboard_state: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    reply: str
    config_json: Optional[Dict[str, Any]] = None


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    result = get_chat_result(payload.message, payload.dashboard_state)
    return result
from pathlib import Path
from typing import Optional
import requests

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent
KB_PATH = BASE_DIR / "knowledge_base.txt"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.1"

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


class ChatResponse(BaseModel):
    reply: str


def load_project_knowledge() -> str:
    if KB_PATH.exists():
        return KB_PATH.read_text(encoding="utf-8")
    return ""


PROJECT_KB = load_project_knowledge()

MUSIC_KNOWLEDGE = {
    "major chord": "A major chord contains a root, major third, and perfect fifth.",
    "minor chord": "A minor chord contains a root, minor third, and perfect fifth.",
    "major scale": "A major scale follows the pattern whole, whole, half, whole, whole, whole, half.",
    "minor scale": "A natural minor scale follows the pattern whole, half, whole, whole, half, whole, whole.",
    "tempo": "Tempo is the speed of music, usually measured in BPM.",
    "bpm": "BPM means beats per minute and controls how fast or slow the music plays.",
    "rhythm": "Rhythm is the timing pattern of notes and beats in music.",
    "melody": "Melody is the main sequence of notes that forms the tune.",
    "harmony": "Harmony is the combination of notes that support the melody.",
    "scale": "A scale is an ordered set of notes used to build melodies and harmonies.",
    "midi": "MIDI is a symbolic music format that stores notes, timing, velocity, and instrument data rather than raw audio.",
    "chords": "Chords are groups of notes played together to create harmony.",
    "bass": "Bass usually provides low-frequency support and helps define harmony and groove.",
    "drums": "Drums provide rhythm and percussion patterns.",
    "markov": "A Markov-based music generator predicts the next note or event based on previous musical events.",
    "markov order": "Markov order controls how much previous note history is used when predicting the next musical event.",
    "genre": "Genre changes the style of generated music output.",
    "note limit": "Note limit controls how many musical events or notes are generated.",
    "download midi": "Download MIDI exports the generated output as a MIDI file.",
    "save session": "Save Session stores the current generated output for later use."
}


def simple_project_search(message: str):
    text = message.lower()
    lines = [line.strip() for line in PROJECT_KB.splitlines() if line.strip()]

    scored = []
    words = [w for w in text.replace("?", "").replace(",", "").split() if len(w) > 2]

    for line in lines:
        score = 0
        lower_line = line.lower()
        for word in words:
            if word in lower_line:
                score += 1
        if score > 0:
            scored.append((score, line))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [line for _, line in scored[:5]]


def rule_based_music_answer(message: str) -> Optional[str]:
    text = message.lower()
    for key, value in MUSIC_KNOWLEDGE.items():
        if key in text:
            return value
    return None


def build_context(message: str) -> str:
    matched_project_lines = simple_project_search(message)

    context_parts = []

    if PROJECT_KB:
        context_parts.append("Melody Matrix project knowledge:")
        if matched_project_lines:
            context_parts.extend([f"- {line}" for line in matched_project_lines])
        else:
            context_parts.append("- No direct project match found, but use general Melody Matrix context.")

    context_parts.append("\nMusic knowledge:")
    for k, v in MUSIC_KNOWLEDGE.items():
        context_parts.append(f"- {k}: {v}")

    return "\n".join(context_parts)


def ask_ollama(user_message: str, context: str) -> str:
    prompt = f"""
You are Melody Matrix Assistant.

Your job:
1. Answer questions about the Melody Matrix system and dashboard using the provided project context.
2. Answer music-related questions clearly and simply.
3. If the user asks about a Melody Matrix control like BPM, Markov order, genre, scale, note limit, melody, bass, drums, chords, save, or download, prioritize the project context.
4. If the user asks about music theory, answer accurately using the music knowledge.
5. Keep answers concise, friendly, and practical.
6. If you do not know something, say so instead of inventing.

Context:
{context}

User question:
{user_message}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )
    response.raise_for_status()
    data = response.json()
    return data.get("response", "").strip()


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    message = payload.message.strip()

    if not message:
        return {"reply": "Please enter a message."}

    context = build_context(message)

    try:
        ai_reply = ask_ollama(message, context)
        if ai_reply:
            return {"reply": ai_reply}
    except Exception:
        pass

    matched_project_lines = simple_project_search(message)
    if matched_project_lines:
        return {
            "reply": "Based on Melody Matrix: " + " ".join(matched_project_lines[:3])
        }

    music_reply = rule_based_music_answer(message)
    if music_reply:
        return {"reply": music_reply}

    return {
        "reply": (
            "I can help with Melody Matrix features like BPM, Markov order, genre, scale, "
            "note limit, melody, bass, drums, chords, saving, and MIDI export. "
            "I can also answer music questions about chords, scales, rhythm, melody, harmony, and MIDI."
        )
    }
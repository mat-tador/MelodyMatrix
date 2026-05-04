import os
from pathlib import Path
from typing import Optional, Dict, Any
import json
import requests

# -----------------------------
# CONFIG
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
KB_PATH = BASE_DIR / "knowledge_base.txt"

# ✅ FIX: Use ENV, do NOT overwrite later
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = "llama3.1"

# ✅ TEST MODE for CI/CD
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"


# -----------------------------
# LOAD KNOWLEDGE BASE
# -----------------------------
def load_project_knowledge() -> str:
    if KB_PATH.exists():
        return KB_PATH.read_text(encoding="utf-8")
    return ""


PROJECT_KB = load_project_knowledge()


# -----------------------------
# MUSIC KNOWLEDGE
# -----------------------------
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
    "midi": "MIDI stores notes and timing data instead of audio.",
    "chords": "Chords are groups of notes played together.",
    "bass": "Bass provides low-frequency support.",
    "drums": "Drums provide rhythm and percussion.",
    "markov": "A Markov model predicts next notes from previous notes.",
    "markov order": "Higher order uses more previous notes."
}


# -----------------------------
# SEARCH
# -----------------------------
def simple_project_search(message: str):
    text = message.lower()
    lines = [line.strip() for line in PROJECT_KB.splitlines() if line.strip()]

    words = [w for w in text.replace("?", "").replace(",", "").split() if len(w) > 2]

    scored = []
    for line in lines:
        score = sum(1 for word in words if word in line.lower())
        if score > 0:
            scored.append((score, line))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [line for _, line in scored[:5]]


# -----------------------------
# RULE BASED ANSWER
# -----------------------------
def rule_based_music_answer(message: str) -> Optional[str]:
    text = message.lower()
    for key, value in MUSIC_KNOWLEDGE.items():
        if key in text:
            return value
    return None


# -----------------------------
# CONTEXT
# -----------------------------
def build_context(message: str, dashboard_state: Optional[Dict[str, Any]] = None) -> str:
    matched = simple_project_search(message)

    context = []

    if PROJECT_KB:
        context.append("Melody Matrix knowledge:")
        context.extend([f"- {m}" for m in matched] or ["- No match found"])

    if dashboard_state:
        context.append("\nDashboard state:")
        context.append(json.dumps(dashboard_state, indent=2))

    return "\n".join(context)


# -----------------------------
# OLLAMA CALL
# -----------------------------
def ask_ollama(user_message: str, context: str) -> str:
    # ✅ TEST MODE: no real API call
    if TEST_MODE:
        return "Test response from AI"

    prompt = f"{context}\n\nUser: {user_message}"

    try:
        res = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        res.raise_for_status()
        return res.json().get("response", "").strip()
    except Exception:
        return ""


# -----------------------------
# CONFIG DETECTION
# -----------------------------
def wants_config_preset(message: str) -> bool:
    triggers = ["config", "preset", "json", "settings", "sound like"]
    return any(t in message.lower() for t in triggers)


# -----------------------------
# RULE CONFIG
# -----------------------------
def preset_from_prompt(message: str, dashboard_state=None) -> Dict[str, Any]:
    base = {
        "preset_name": "custom",
        "scale": "D Minor",
        "bpm": 72,
        "markov_order": 3
    }

    if "sad" in message.lower():
        base.update({"scale": "A Minor", "bpm": 65})

    if "epic" in message.lower():
        base.update({"bpm": 100})

    return base


# -----------------------------
# AI CONFIG
# -----------------------------
def try_ai_config_preset(message: str, dashboard_state=None):
    # ✅ TEST MODE SAFE RESPONSE
    if TEST_MODE:
        return {
            "preset_name": "test_preset",
            "bpm": 120,
            "scale": "C Major",
            "markov_order": 2
        }

    context = build_context(message, dashboard_state)

    try:
        res = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": context,
                "stream": False
            },
            timeout=30
        )
        data = res.json()
        return json.loads(data.get("response", "{}"))
    except Exception:
        return None


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def get_chat_result(message: str, dashboard_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    message = message.strip()

    if not message:
        return {"reply": "Please enter a message.", "config_json": None}

    # CONFIG
    if wants_config_preset(message):
        config = try_ai_config_preset(message, dashboard_state)

        if not config:
            config = preset_from_prompt(message, dashboard_state)

        return {
            "reply": "Generated a configuration preset.",
            "config_json": config
        }

    # NORMAL CHAT
    context = build_context(message, dashboard_state)
    reply = ask_ollama(message, context)

    if reply:
        return {"reply": reply, "config_json": None}

    # FALLBACK
    proj = simple_project_search(message)
    if proj:
        return {"reply": " ".join(proj[:2]), "config_json": None}

    music = rule_based_music_answer(message)
    if music:
        return {"reply": music, "config_json": None}

    return {
        "reply": "Ask about Melody Matrix or request a config preset.",
        "config_json": None
    }
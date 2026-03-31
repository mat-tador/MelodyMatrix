from pathlib import Path
from typing import Optional, Dict, Any
import json
import requests

BASE_DIR = Path(__file__).resolve().parent
KB_PATH = BASE_DIR / "knowledge_base.txt"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.1"


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


def build_context(message: str, dashboard_state: Optional[Dict[str, Any]] = None) -> str:
    matched_project_lines = simple_project_search(message)
    context_parts = []

    if PROJECT_KB:
        context_parts.append("Melody Matrix project knowledge:")
        if matched_project_lines:
            context_parts.extend([f"- {line}" for line in matched_project_lines])
        else:
            context_parts.append("- No direct project match found, but use general Melody Matrix context.")

    if dashboard_state:
        context_parts.append("\nCurrent dashboard configuration:")
        context_parts.append(json.dumps(dashboard_state, indent=2))

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


def wants_config_preset(message: str) -> bool:
    text = message.lower()
    triggers = [
        "config my system",
        "configure my system",
        "give me a config",
        "give me json",
        "preset",
        "settings json",
        "config json",
        "sound like",
        "make it sound like",
    ]
    return any(trigger in text for trigger in triggers)


def preset_from_prompt(message: str, dashboard_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    text = message.lower()

    base = {
        "preset_name": "custom_preset",
        "description": "Generated preset for Melody Matrix",
        "genre": "cinematic",
        "scale": "D Minor",
        "bpm": 72,
        "note_limit": 64,
        "markov_order": 3,
        "instruments": {
            "melody": True,
            "bass": True,
            "drums": False,
            "chords": True
        },
        "mix": {
            "melody_density": 0.55,
            "bass_density": 0.35,
            "chord_density": 0.65,
            "drum_density": 0.0
        },
        "style_tags": ["cinematic", "emotional", "orchestral"],
        "apply_notes": "Import or manually set these values in the dashboard."
    }

    # Safer substitute for copyrighted-style imitation requests
    if "titanic" in text:
        base.update({
            "preset_name": "cinematic_oceanic_romance",
            "description": "Inspired by a sweeping romantic oceanic film-ballad mood, using broad cinematic traits rather than copying a specific soundtrack.",
            "genre": "cinematic",
            "scale": "D Minor",
            "bpm": 68,
            "note_limit": 72,
            "markov_order": 4,
            "instruments": {
                "melody": True,
                "bass": True,
                "drums": False,
                "chords": True
            },
            "mix": {
                "melody_density": 0.42,
                "bass_density": 0.28,
                "chord_density": 0.78,
                "drum_density": 0.0
            },
            "style_tags": [
                "romantic",
                "oceanic",
                "cinematic",
                "lush_strings",
                "nostalgic",
                "slow_build"
            ]
        })
        return base

    if "sad" in text or "emotional" in text:
        base.update({
            "preset_name": "emotional_cinematic",
            "genre": "ambient",
            "scale": "A Minor",
            "bpm": 70,
            "note_limit": 60,
            "markov_order": 3,
            "style_tags": ["emotional", "ambient", "cinematic"]
        })
        return base

    if "epic" in text:
        base.update({
            "preset_name": "epic_cinematic",
            "genre": "cinematic",
            "scale": "E Minor",
            "bpm": 96,
            "note_limit": 80,
            "markov_order": 4,
            "instruments": {
                "melody": True,
                "bass": True,
                "drums": True,
                "chords": True
            },
            "mix": {
                "melody_density": 0.6,
                "bass_density": 0.5,
                "chord_density": 0.8,
                "drum_density": 0.45
            },
            "style_tags": ["epic", "cinematic", "dramatic", "trailer_like"]
        })
        return base

    if "jazz" in text:
        base.update({
            "preset_name": "smooth_jazz",
            "genre": "jazz",
            "scale": "C Major",
            "bpm": 92,
            "note_limit": 56,
            "markov_order": 2,
            "instruments": {
                "melody": True,
                "bass": True,
                "drums": True,
                "chords": True
            },
            "style_tags": ["jazz", "warm", "smooth"]
        })
        return base

    if dashboard_state:
        base["current_dashboard_state"] = dashboard_state

    return base


def try_ai_config_preset(message: str, dashboard_state: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    context = build_context(message, dashboard_state)
    prompt = f"""
You are Melody Matrix Assistant.

Return only valid JSON.
Do not include markdown fences.
Do not include commentary outside JSON.

Goal:
Generate a Melody Matrix config preset based on the user request.

Required JSON schema:
{{
  "preset_name": "string",
  "description": "string",
  "genre": "string",
  "scale": "string",
  "bpm": 0,
  "note_limit": 0,
  "markov_order": 0,
  "instruments": {{
    "melody": true,
    "bass": true,
    "drums": false,
    "chords": true
  }},
  "mix": {{
    "melody_density": 0.0,
    "bass_density": 0.0,
    "chord_density": 0.0,
    "drum_density": 0.0
  }},
  "style_tags": ["string"],
  "apply_notes": "string"
}}

Important:
- If the user references a copyrighted work like Titanic, do not imitate it directly.
- Instead, produce a broad high-level mood-based preset inspired by cinematic traits only.
- Keep bpm between 50 and 160.
- Keep note_limit between 16 and 128.
- Keep markov_order between 1 and 6.

Context:
{context}

User request:
{message}
"""

    try:
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
        raw = data.get("response", "").strip()
        parsed = json.loads(raw)
        return parsed
    except Exception:
        return None


def get_chat_result(message: str, dashboard_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    message = message.strip()

    if not message:
        return {"reply": "Please enter a message.", "config_json": None}

    if wants_config_preset(message):
        config = try_ai_config_preset(message, dashboard_state)
        if not config:
            config = preset_from_prompt(message, dashboard_state)

        return {
            "reply": "I generated a preset JSON for that mood. You can download it and apply it to the dashboard.",
            "config_json": config
        }

    context = build_context(message, dashboard_state)

    try:
        ai_reply = ask_ollama(message, context)
        if ai_reply:
            return {"reply": ai_reply, "config_json": None}
    except Exception:
        pass

    matched_project_lines = simple_project_search(message)
    if matched_project_lines:
        return {
            "reply": "Based on Melody Matrix: " + " ".join(matched_project_lines[:3]),
            "config_json": None
        }

    music_reply = rule_based_music_answer(message)
    if music_reply:
        return {"reply": music_reply, "config_json": None}

    return {
        "reply": (
            "I can help with Melody Matrix features like BPM, Markov order, genre, scale, "
            "note limit, melody, bass, drums, chords, saving, and MIDI export. "
            "I can also generate config JSON presets for moods and styles."
        ),
        "config_json": None
    }
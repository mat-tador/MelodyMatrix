from flask import Blueprint, jsonify, request, render_template, send_from_directory
import os
from music_generator import (
    generate_sequence,
    get_graph_data,
    BASE_CHAINS_BY_GENRE,
    SCALE_MAPS,
    INSTRUMENT_TYPES,
)

api = Blueprint("api", __name__, url_prefix="/api")


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def error(message: str, status: int = 400):
    return jsonify({"ok": False, "error": message}), status


def ok(data: dict, status: int = 200):
    return jsonify({"ok": True, **data}), status


# ---------------------------------------------------------------------------
# Frontend pages (serve HTML files from templates/)
# ---------------------------------------------------------------------------

def register_routes(app):
    # ---- static HTML pages ------------------------------------------------
    @app.route("/")
    @app.route("/dashboard")
    def dashboard():
        return render_template("dashboard.html")

    @app.route("/generate")
    def generate_page():
        return render_template("generate.html")

    @app.route("/saved-outputs")
    def saved_outputs():
        return render_template("saved-outputs.html")

    @app.route("/settings")
    def settings():
        return render_template("settings.html")

    # ---- register API blueprint -------------------------------------------
    app.register_blueprint(api)


# ---------------------------------------------------------------------------
# API — Meta
# ---------------------------------------------------------------------------

@api.route("/health", methods=["GET"])
def health():
    """Quick liveness check."""
    return ok({"status": "running", "version": "1.0.0"})


@api.route("/meta", methods=["GET"])
def meta():
    """Return all valid genres, scales, and instrument lists."""
    return ok({
        "genres": list(BASE_CHAINS_BY_GENRE.keys()),
        "scales": list(SCALE_MAPS.keys()),
        "instruments": INSTRUMENT_TYPES,
        "orders": [1, 2, 3],
    })


# ---------------------------------------------------------------------------
# API — Generate
# ---------------------------------------------------------------------------

@api.route("/generate", methods=["POST"])
def generate():
    """
    Generate a Markov music sequence.

    Body (JSON):
        genre       str     required
        scale       str     required
        order       int     1 | 2 | 3   (default 2)
        steps       int     1–200       (default 16)
        instruments list    optional, defaults to all four
        seed        int     optional, for reproducibility
    """
    body = request.get_json(silent=True) or {}

    genre = body.get("genre")
    scale = body.get("scale")
    if not genre or not scale:
        return error("'genre' and 'scale' are required.")

    try:
        result = generate_sequence(
            genre=genre,
            scale=scale,
            order=int(body.get("order", 2)),
            steps=int(body.get("steps", 16)),
            active_instruments=body.get("instruments") or None,
            seed=body.get("seed"),
        )
    except (ValueError, KeyError) as exc:
        return error(str(exc))

    return ok({"result": result})


# ---------------------------------------------------------------------------
# API — Step (single Markov step for live playback sync)
# ---------------------------------------------------------------------------

@api.route("/step", methods=["POST"])
def step():
    """
    Advance the Markov walker by one step for each active instrument.

    Body (JSON):
        genre       str
        scale       str
        order       int
        current     dict   { melody: "Do", bass: "Do", ... }
        instruments list   which instruments to step
    """
    body = request.get_json(silent=True) or {}

    genre = body.get("genre")
    scale = body.get("scale")
    order = int(body.get("order", 2))
    current_states = body.get("current", {})
    instruments = body.get("instruments", INSTRUMENT_TYPES)

    if not genre or not scale:
        return error("'genre' and 'scale' are required.")
    if genre not in BASE_CHAINS_BY_GENRE:
        return error(f"Unknown genre: {genre}")

    from music_generator import get_order_chain, get_label, get_node_list
    import random

    new_states = {}
    labels = {}

    for inst in instruments:
        if inst not in INSTRUMENT_TYPES:
            continue
        chain = get_order_chain(genre, inst, order)
        nodes = get_node_list(genre, inst)
        current = current_states.get(inst, nodes[0])
        options = chain.get(current, nodes)
        nxt = random.choice(options)
        new_states[inst] = nxt
        labels[inst] = get_label(nxt, scale)

    return ok({"states": new_states, "labels": labels})


# ---------------------------------------------------------------------------
# API — Graph data
# ---------------------------------------------------------------------------

@api.route("/graph", methods=["GET"])
def graph():
    """
    Return Markov graph node/edge data for a given genre + scale + order.

    Query params: genre, scale, order (default 2)
    """
    genre = request.args.get("genre")
    scale = request.args.get("scale")
    order = int(request.args.get("order", 2))

    if not genre or not scale:
        return error("'genre' and 'scale' query params are required.")

    try:
        data = get_graph_data(genre, scale, order)
    except ValueError as exc:
        return error(str(exc))

    return ok({"graph": data})


# ---------------------------------------------------------------------------
# API — Settings (server-side persistence, optional — frontend uses localStorage)
# ---------------------------------------------------------------------------

# In-memory store (replace with a DB in production)
_server_settings: dict = {}


@api.route("/settings", methods=["GET"])
def get_settings():
    return ok({"settings": _server_settings})


@api.route("/settings", methods=["POST"])
def save_settings():
    body = request.get_json(silent=True) or {}
    _server_settings.update(body)
    return ok({"settings": _server_settings, "message": "Settings saved."})


@api.route("/settings/reset", methods=["POST"])
def reset_settings():
    _server_settings.clear()
    return ok({"settings": _server_settings, "message": "Settings reset to defaults."})


# ---------------------------------------------------------------------------
# API — Sessions (server-side saved outputs)
# ---------------------------------------------------------------------------

_saved_sessions: list = []


@api.route("/sessions", methods=["GET"])
def list_sessions():
    return ok({"sessions": _saved_sessions, "count": len(_saved_sessions)})


@api.route("/sessions", methods=["POST"])
def save_session():
    body = request.get_json(silent=True) or {}
    import time
    session = {
        "id": int(time.time() * 1000),
        **body,
    }
    _saved_sessions.insert(0, session)
    # Keep at most 100 server-side
    while len(_saved_sessions) > 100:
        _saved_sessions.pop()
    return ok({"session": session, "message": "Session saved."})


@api.route("/sessions/<int:session_id>", methods=["DELETE"])
def delete_session(session_id: int):
    global _saved_sessions
    before = len(_saved_sessions)
    _saved_sessions = [s for s in _saved_sessions if s.get("id") != session_id]
    if len(_saved_sessions) == before:
        return error(f"Session {session_id} not found.", 404)
    return ok({"message": f"Session {session_id} deleted."})


@api.route("/sessions", methods=["DELETE"])
def clear_sessions():
    _saved_sessions.clear()
    return ok({"message": "All sessions cleared."})
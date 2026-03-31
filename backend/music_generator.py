import pretty_midi
import os
import random

OUTPUT_FOLDER = "data/generated_music"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def generate_music(length=100):
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)

    time = 0

    for _ in range(length):
        pitch = random.randint(60, 72)
        duration = random.uniform(0.2, 0.5)

        note = pretty_midi.Note(
            velocity=100,
            pitch=pitch,
            start=time,
            end=time + duration
        )

        instrument.notes.append(note)
        time += duration

    midi.instruments.append(instrument)

    output_path = os.path.join(OUTPUT_FOLDER, "generated.mid")
    midi.write(output_path)

    return output_path
import random
from typing import Dict, List, Optional


# Markov chain data — mirrors dashboard.html baseChainsByGenre

BASE_CHAINS_BY_GENRE: Dict[str, Dict[str, Dict[str, List[str]]]] = {
    "Techno-Jazz": {
        "melody": {
            "Do": ["Mib", "Sol", "Fa"],
            "Re": ["Do", "Mib"],
            "Mib": ["Fa", "Sol", "Do"],
            "Fa": ["Mib", "Sol"],
            "Sol": ["Sib", "Do_Alto", "Fa"],
            "Sib": ["Sol", "Do_Alto"],
            "Do_Alto": ["Sib", "Sol"],
        },
        "bass": {
            "Do": ["Do", "Do", "Mib", "Pausa"],
            "Mib": ["Fa", "Do"],
            "Fa": ["Sol", "Do"],
            "Sol": ["Do", "Do", "Sib"],
            "Sib": ["Sol", "Do"],
            "Pausa": ["Do", "Sol"],
        },
        "drums": {
            "Closed": ["Closed", "Open", "Pausa"],
            "Open": ["Closed", "Pausa"],
            "Pausa": ["Closed", "Open"],
        },
        "chords": {
            "i": ["iv", "v", "VI"],
            "iv": ["i", "v"],
            "v": ["i", "VII"],
            "VI": ["iv", "VII"],
            "VII": ["i", "v"],
        },
    },
    "Ambient": {
        "melody": {
            "Do": ["Fa", "Sol", "Mib"],
            "Re": ["Do", "Fa"],
            "Mib": ["Do", "Fa", "Sol"],
            "Fa": ["Sol", "Do_Alto", "Mib"],
            "Sol": ["Fa", "Do_Alto"],
            "Sib": ["Fa", "Sol"],
            "Do_Alto": ["Sol", "Fa", "Mib"],
        },
        "bass": {
            "Do": ["Pausa", "Mib", "Do"],
            "Mib": ["Do", "Fa"],
            "Fa": ["Pausa", "Sol"],
            "Sol": ["Do", "Pausa"],
            "Sib": ["Fa", "Do"],
            "Pausa": ["Do", "Fa", "Sol"],
        },
        "drums": {
            "Closed": ["Pausa", "Closed", "Open"],
            "Open": ["Pausa", "Closed"],
            "Pausa": ["Closed", "Pausa", "Open"],
        },
        "chords": {
            "i": ["VI", "iv", "i"],
            "iv": ["i", "VI"],
            "v": ["i"],
            "VI": ["i", "VII"],
            "VII": ["i", "iv"],
        },
    },
    "House": {
        "melody": {
            "Do": ["Sol", "Fa", "Do_Alto"],
            "Re": ["Fa", "Sol"],
            "Mib": ["Sol", "Do"],
            "Fa": ["Do", "Sol", "Do_Alto"],
            "Sol": ["Do", "Fa", "Sib"],
            "Sib": ["Do_Alto", "Sol"],
            "Do_Alto": ["Sol", "Fa", "Do"],
        },
        "bass": {
            "Do": ["Do", "Sol", "Pausa"],
            "Mib": ["Do", "Fa"],
            "Fa": ["Sol", "Do"],
            "Sol": ["Do", "Sol", "Sib"],
            "Sib": ["Do", "Sol"],
            "Pausa": ["Do", "Do", "Sol"],
        },
        "drums": {
            "Closed": ["Closed", "Closed", "Open"],
            "Open": ["Closed", "Closed"],
            "Pausa": ["Closed", "Open"],
        },
        "chords": {
            "i": ["VI", "III", "VII"],
            "III": ["VI", "VII"],
            "VI": ["i", "III"],
            "VII": ["i", "VI"],
        },
    },
    "Hip Hop": {
        "melody": {
            "Do": ["Mib", "Fa", "Do"],
            "Re": ["Do", "Fa"],
            "Mib": ["Do", "Sol"],
            "Fa": ["Do", "Mib", "PausaMelody"],
            "Sol": ["Fa", "Mib", "Do"],
            "Sib": ["Sol", "Fa"],
            "Do_Alto": ["Sol", "Mib"],
        },
        "bass": {
            "Do": ["Do", "Pausa", "Mib"],
            "Mib": ["Do", "Pausa"],
            "Fa": ["Sol", "Do"],
            "Sol": ["Do", "Pausa", "Sib"],
            "Sib": ["Do", "Sol"],
            "Pausa": ["Do", "Mib", "Sol"],
        },
        "drums": {
            "Closed": ["Closed", "Pausa", "Open"],
            "Open": ["Closed", "Pausa"],
            "Pausa": ["Closed", "Closed", "Open"],
        },
        "chords": {
            "i": ["VII", "VI", "i"],
            "VI": ["i", "VII"],
            "VII": ["i", "VI"],
            "iv": ["i"],
        },
    },
}

SCALE_MAPS: Dict[str, Dict[str, str]] = {
    "C Minor": {
        "Do": "Do", "Re": "Re", "Mib": "Mib", "Fa": "Fa", "Sol": "Sol",
        "Sib": "Sib", "Do_Alto": "Do_Alto", "Pausa": "Pausa",
        "Closed": "Closed", "Open": "Open", "PausaMelody": "Rest",
        "i": "Cm", "III": "Eb", "iv": "Fm", "v": "Gm", "VI": "Ab", "VII": "Bb",
    },
    "C Major": {
        "Do": "Do", "Re": "Re", "Mib": "Mi", "Fa": "Fa", "Sol": "Sol",
        "Sib": "La", "Do_Alto": "Ti", "Pausa": "Pausa",
        "Closed": "Closed", "Open": "Open", "PausaMelody": "Rest",
        "i": "C", "III": "Em", "iv": "F", "v": "G", "VI": "Am", "VII": "Bdim",
    },
}

DEFAULT_STATE = {"melody": "Do", "bass": "Do", "drums": "Closed", "chords": "i"}

INSTRUMENT_TYPES = ["melody", "bass", "drums", "chords"]



# Chain building helpers (mirrors dashboard.html JS functions)


def build_order_chain(
    base: Dict[str, List[str]], order: int, instrument_type: str
) -> Dict[str, List[str]]:
    if order == 1:
        return base

    adjusted: Dict[str, List[str]] = {}
    if order == 2:
        for key, vals in base.items():
            adjusted[key] = [vals[0], vals[0], *vals] if len(vals) > 1 else vals[:]
        return adjusted

    all_keys = list(base.keys())
    for key, vals in base.items():
        extras_count = 1 if instrument_type == "drums" else 2
        extras = [k for k in all_keys if k != key][:extras_count]
        if len(vals) > 1:
            adjusted[key] = [vals[0], vals[0], vals[1], *vals, *extras]
        else:
            adjusted[key] = [*vals, *extras]
    return adjusted


def apply_genre_character(
    chain: Dict[str, List[str]], genre: str, instrument_type: str
) -> Dict[str, List[str]]:
    adjusted = {k: v[:] for k, v in chain.items()}

    if genre == "Ambient":
        for key in adjusted:
            adjusted[key].append(key)

    elif genre == "House":
        if instrument_type == "drums":
            for key in adjusted:
                adjusted[key].append("Closed")
        if instrument_type == "bass" and "Do" in adjusted:
            adjusted["Do"] = ["Do", "Do", "Sol", "Pausa"] + adjusted["Do"]
        if instrument_type == "chords" and "i" in adjusted:
            adjusted["i"] = ["VI", "VI"] + adjusted["i"]

    elif genre == "Hip Hop":
        if instrument_type == "bass" and "Pausa" in adjusted:
            adjusted["Pausa"] = ["Do", "Mib", "Sol", "Pausa"]
        if instrument_type == "melody":
            for key in adjusted:
                adjusted[key].append("PausaMelody")
        if instrument_type == "chords" and "i" in adjusted:
            adjusted["i"] = ["VII", "VI"] + adjusted["i"]

    elif genre == "Techno-Jazz":
        if instrument_type == "melody" and "Sol" in adjusted:
            adjusted["Sol"] = ["Sib", "Do_Alto", "Fa", "Mib"] + adjusted["Sol"]
        if instrument_type == "chords" and "i" in adjusted:
            adjusted["i"] = ["iv", "v", "VI"] + adjusted["i"]

    return adjusted


def get_order_chain(genre: str, instrument_type: str, order: int) -> Dict[str, List[str]]:
    base = BASE_CHAINS_BY_GENRE[genre][instrument_type]
    chain = build_order_chain(base, order, instrument_type)
    return apply_genre_character(chain, genre, instrument_type)


def get_node_list(genre: str, instrument_type: str) -> List[str]:
    nodes = list(BASE_CHAINS_BY_GENRE[genre][instrument_type].keys())
    if instrument_type == "melody" and genre == "Hip Hop" and "PausaMelody" not in nodes:
        nodes.append("PausaMelody")
    return nodes


def get_label(key: str, scale: str) -> str:
    return SCALE_MAPS.get(scale, {}).get(key, key).replace("_", " ")


# ---------------------------------------------------------------------------
# Core generation function
# ---------------------------------------------------------------------------

def generate_sequence(
    genre: str,
    scale: str,
    order: int,
    steps: int,
    active_instruments: Optional[List[str]] = None,
    seed: Optional[int] = None,
) -> Dict:
    """
    Generate a Markov-chain music sequence.

    Parameters
    ----------
    genre           : One of the keys in BASE_CHAINS_BY_GENRE
    scale           : "C Minor" or "C Major"
    order           : Markov order 1, 2, or 3
    steps           : Number of steps to generate per instrument
    active_instruments : List of instruments to generate; defaults to all
    seed            : Optional random seed for reproducibility

    Returns
    -------
    dict with keys: genre, scale, order, steps, sequences (per instrument),
                    raw_sequences, metadata
    """
    if seed is not None:
        random.seed(seed)

    if genre not in BASE_CHAINS_BY_GENRE:
        raise ValueError(f"Unknown genre '{genre}'. Choose from: {list(BASE_CHAINS_BY_GENRE)}")
    if scale not in SCALE_MAPS:
        raise ValueError(f"Unknown scale '{scale}'. Choose from: {list(SCALE_MAPS)}")
    if order not in (1, 2, 3):
        raise ValueError("Order must be 1, 2, or 3.")
    if not (1 <= steps <= 200):
        raise ValueError("Steps must be between 1 and 200.")

    instruments = active_instruments or INSTRUMENT_TYPES

    raw_sequences: Dict[str, List[str]] = {}
    sequences: Dict[str, List[str]] = {}

    for inst in instruments:
        if inst not in INSTRUMENT_TYPES:
            continue

        chain = get_order_chain(genre, inst, order)
        nodes = get_node_list(genre, inst)
        current = DEFAULT_STATE.get(inst, nodes[0])
        if current not in nodes:
            current = nodes[0]

        raw: List[str] = [current]
        for _ in range(steps - 1):
            options = chain.get(current, nodes)
            current = random.choice(options)
            raw.append(current)

        raw_sequences[inst] = raw
        sequences[inst] = [get_label(k, scale) for k in raw]

    return {
        "genre": genre,
        "scale": scale,
        "order": order,
        "steps": steps,
        "active_instruments": instruments,
        "sequences": sequences,
        "raw_sequences": raw_sequences,
        "metadata": {
            "available_genres": list(BASE_CHAINS_BY_GENRE.keys()),
            "available_scales": list(SCALE_MAPS.keys()),
        },
    }


def get_graph_data(genre: str, scale: str, order: int) -> Dict:
    """
    Return graph node/edge data so the frontend can render the Markov graph.
    """
    if genre not in BASE_CHAINS_BY_GENRE:
        raise ValueError(f"Unknown genre: {genre}")

    graph_data = {}
    for inst in INSTRUMENT_TYPES:
        chain = get_order_chain(genre, inst, order)
        nodes = get_node_list(genre, inst)
        edges = []
        for src, targets in chain.items():
            for tgt in set(targets):
                edges.append({"from": src, "to": tgt, "label_from": get_label(src, scale), "label_to": get_label(tgt, scale)})
        graph_data[inst] = {
            "nodes": [{"id": n, "label": get_label(n, scale)} for n in nodes],
            "edges": edges,
            "default_state": DEFAULT_STATE.get(inst, nodes[0]),
        }

    return {"genre": genre, "scale": scale, "order": order, "graphs": graph_data}

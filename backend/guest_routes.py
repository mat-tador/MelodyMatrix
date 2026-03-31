from flask import Blueprint, request, jsonify
import os
from music_generator import generate_music
from midi_parser import parse_midi

guest_bp = Blueprint('guest', __name__)

UPLOAD_FOLDER = "data/input_midi"
OUTPUT_FOLDER = "data/generated_music"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)



@guest_bp.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        length = data.get("length", 100)

        output_file = generate_music(length)

        return jsonify({
            "message": "Music generated successfully",
            "file": output_file
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest_bp.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        notes = parse_midi(filepath)

        return jsonify({
            "message": "File uploaded successfully",
            "notes_count": len(notes)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
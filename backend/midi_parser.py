from mido import MidiFile

def parse_midi(file_path):
    try:
        midi = MidiFile(file_path)
        notes = []

        for track in midi.tracks:
            for msg in track:
                if msg.type == 'note_on' and msg.velocity > 0:
                    notes.append({
                        "note": msg.note,
                        "velocity": msg.velocity,
                        "time": msg.time
                    })

        return notes

    except Exception as e:
        print("Error parsing MIDI:", e)
        return []
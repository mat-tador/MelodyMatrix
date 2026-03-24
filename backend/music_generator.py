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
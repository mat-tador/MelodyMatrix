from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from enum import Enum
from collections import Counter, defaultdict
import random
import time

class Instrument(Enum):
    # We keep the enum for reference
    PIANO = range(0, 8)
    CHROMATIC_PERCUSSION = range(8, 16)
    ORGAN = range(16, 24)
    GUITAR = range(24, 32)
    BASS = range(32, 40)
    STRINGS = range(40, 48)
    BRASS = range(56, 64)
    REEDS = range(64, 72)
    PIPE = range(72, 80)
    SYNTH_LEAD = range(80, 88)
    SYNTH_PAD = range(88, 96)
    SYNTH_EFFECTS = range(96, 104)
    ETHNIC = range(104, 112)
    PERCUSSIVE = range(112, 120)
    SOUND_EFFECTS = range(120, 128)

def get_note_name(midi_note):
    """Converts a MIDI note number (0-127) to a standard musical pitch."""
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (midi_note // 12) - 1
    note_name = notes[midi_note % 12]
    return f"{note_name}{octave}"

def get_piano_track(mid, specific_program=0):
    """Scans the MIDI file and returns the first track matching the EXACT program number."""
    for track in mid.tracks[1:]:
        for msg in track:
            if msg.type == 'program_change':
                if msg.program == specific_program:
                    return track
    return None

def generate_markov(midi_file_path, order, specific_program=0):
    """Core engine: Generates a Markov chain of the specified order for a specific instrument."""
    try:
        mid = MidiFile(midi_file_path)
    except FileNotFoundError:
        print(f"Error: Could not find file {midi_file_path}")
        return None

    piano_track = get_piano_track(mid, specific_program)
    
    if not piano_track:
        print(f"No track found using exact program number: {specific_program}")
        return None
        
    note_sequence = []
    for msg in piano_track:
        if msg.type == 'note_on' and msg.velocity > 0:
            note_sequence.append(msg.note)
            
    if len(note_sequence) <= order:
        print(f"Not enough notes in this track to generate an order {order} chain.")
        return None

    markov_chain = defaultdict(list)
    for i in range(len(note_sequence) - order):
        state = tuple(note_sequence[i:i + order])
        next_note = note_sequence[i + order]
        markov_chain[state].append(next_note)
        
    return dict(markov_chain)

def generate_first_order_markov(midi_file_path, specific_program=0):
    return generate_markov(midi_file_path, order=1, specific_program=specific_program)

def generate_second_order_markov(midi_file_path, specific_program=0):
    return generate_markov(midi_file_path, order=2, specific_program=specific_program)

def generate_third_order_markov(midi_file_path, specific_program=0):
    return generate_markov(midi_file_path, order=3, specific_program=specific_program)

def generate_music_from_markov(markov_chain, output_filename, num_notes=50, bpm=120):
    """Takes a Markov chain dictionary and generates a new MIDI file."""
    if not markov_chain:
        print("Empty Markov chain. Cannot generate music.")
        return

    # Force a new random seed every time the function is called
    random.seed(time.time())

    new_mid = MidiFile()
    tempo_track = MidiTrack()
    music_track = MidiTrack()
    new_mid.tracks.extend([tempo_track, music_track])

    tempo_track.append(MetaMessage('set_tempo', tempo=bpm2tempo(bpm), time=0))
    music_track.append(Message('program_change', program=0, time=0))

    current_state = random.choice(list(markov_chain.keys()))
    ticks_per_quarter_note = new_mid.ticks_per_beat 

    # Play the initial seed notes
    for note in current_state:
        music_track.append(Message('note_on', note=note, velocity=64, time=0))
        music_track.append(Message('note_off', note=note, velocity=0, time=ticks_per_quarter_note))

    # Generate the rest of the sequence
    for _ in range(num_notes - len(current_state)):
        if current_state not in markov_chain or not markov_chain[current_state]:
            current_state = random.choice(list(markov_chain.keys()))
            
        next_note = random.choice(markov_chain[current_state])
        
        music_track.append(Message('note_on', note=next_note, velocity=64, time=0))
        music_track.append(Message('note_off', note=next_note, velocity=0, time=ticks_per_quarter_note))
        
        current_state = tuple(list(current_state[1:]) + [next_note])

    new_mid.save(output_filename)
    print(f"Generated new track: '{output_filename}' at {bpm} BPM")


if __name__ == "__main__":
    
    file_path = './data/Bohemian_Rhapsody.mid'
    
    # ==========================================
    # SETTINGS
    # ==========================================
    target_instrument = 0   # 0 = Acoustic Grand Piano
    selected_order = 3      # Choose 1, 2, or 3
    # ==========================================
    
    print(f"--- Generating Order {selected_order} Markov Chain for Instrument {target_instrument} ---")
    
    # Route to the correct wrapper function based on the user's selection
    if selected_order == 1:
        markov_chain = generate_first_order_markov(file_path, specific_program=target_instrument)
    elif selected_order == 2:
        markov_chain = generate_second_order_markov(file_path, specific_program=target_instrument)
    elif selected_order == 3:
        markov_chain = generate_third_order_markov(file_path, specific_program=target_instrument)
    else:
        print("Invalid order selected. Please choose 1, 2, or 3.")
        markov_chain = None
    
    if markov_chain:
        print(f"Success! Order {selected_order} chain has {len(markov_chain)} unique states.")
        
        print(f"\nSample of Order {selected_order} Transitions:")
        sample_count = 0
        for state, next_notes in markov_chain.items():
            state_names = tuple(get_note_name(n) for n in state)
            next_names = [get_note_name(n) for n in next_notes]
            print(f"{state_names} -> {next_names[:5]} ... (total {len(next_notes)} transitions)")
            sample_count += 1
            if sample_count >= 3:
                break
        
        print(f"\n--- Generating AI Music (Using Order {selected_order}) ---")
        
        # We automatically update the filename based on the selected order!
        output_file = f'./data/generated_order_{selected_order}.mid'
        
        generate_music_from_markov(
            markov_chain=markov_chain, 
            output_filename=output_file, 
            num_notes=100, 
            bpm=120
        )
        
        print(f"\nDone! Check your ./data/ folder for '{output_file}'.")
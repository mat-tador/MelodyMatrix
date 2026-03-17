import time 
import rtmidi 

'''
This is a preliminary version of the MIDI engine, which should be used just to integrate 
the MIDI sound into the project. IT IS NOT A FINAL VERSION 
'''

def play_chord(out, notes, duration=1.5, velocity=100):
    """Plays a chord by passing an exact list of MIDI notes"""
    # Send 'Note On' for all notes in the chord list
    for note in notes:
        out.send_message([0x90, note, velocity])
        
    time.sleep(duration) # Hold the chord
    
    # Send 'Note Off' to stop the notes
    for note in notes:
        out.send_message([0x80, note, 0])

out = rtmidi.MidiOut()
ports = out.get_ports()
print("Available ports:", ports)

out.open_port(1)

# The Chords
chord_Em7    = [52, 59, 62, 67] # E, B, D, G
chord_G      = [55, 59, 62, 67] # G, B, D, G
chord_D      = [50, 57, 62, 66] # D, A, D, F#
chord_A7sus4 = [57, 64, 62, 67] # A, E, D, G
chord_C      = [48, 52, 55, 60, 64] # C, E, G, C, E

# The Bass Notes
bass_E = 28
bass_G = 31
bass_D = 38
bass_A = 33

# Setup Instruments & Effects
out.send_message([0xC0, 26])      # Ch 1: Acoustic Guitar (Steel)
out.send_message([0xB0, 91, 100]) # Ch 1: Reverb
out.send_message([0xC1, 34])      # Ch 2: Electric Bass (Pick)

with out:
    # --- FIRST PROGRESSION ---
    # 1. Em7 (Kick + Hat)
    out.send_message([0x91, bass_E, 110]) # Bass ON
    out.send_message([0x99, 36, 110])     # Kick ON
    out.send_message([0x99, 42, 90])      # Hat ON
    play_chord(out, chord_Em7)
    out.send_message([0x81, bass_E, 0])   # Bass OFF

    # 2. G (Snare + Hat)
    out.send_message([0x91, bass_G, 110])
    out.send_message([0x99, 38, 110])     # Snare ON
    out.send_message([0x99, 42, 90])      # Hat ON
    play_chord(out, chord_G)
    out.send_message([0x81, bass_G, 0])

    # 3. D (Kick + Hat)
    out.send_message([0x91, bass_D, 110])
    out.send_message([0x99, 36, 110])     
    out.send_message([0x99, 42, 90])      
    play_chord(out, chord_D)
    out.send_message([0x81, bass_D, 0])

    # 4. A7sus4 (Snare + Hat)
    out.send_message([0x91, bass_A, 110])
    out.send_message([0x99, 38, 110])     
    out.send_message([0x99, 42, 90])      
    play_chord(out, chord_A7sus4)
    out.send_message([0x81, bass_A, 0])

    # --- SECOND PROGRESSION ---
    # 1. Em7
    out.send_message([0x91, bass_E, 110])
    out.send_message([0x99, 36, 110])     
    out.send_message([0x99, 42, 90])      
    play_chord(out, chord_Em7)
    out.send_message([0x81, bass_E, 0])   

    # 2. G
    out.send_message([0x91, bass_G, 110])
    out.send_message([0x99, 38, 110])     
    out.send_message([0x99, 42, 90])      
    play_chord(out, chord_G)
    out.send_message([0x81, bass_G, 0])

    # 3. D
    out.send_message([0x91, bass_D, 110])
    out.send_message([0x99, 36, 110])     
    out.send_message([0x99, 42, 90])      
    play_chord(out, chord_D)
    out.send_message([0x81, bass_D, 0])

    # 4. A7sus4
    out.send_message([0x91, bass_A, 110])
    out.send_message([0x99, 38, 110])     
    out.send_message([0x99, 42, 90])      
    play_chord(out, chord_A7sus4)
    out.send_message([0x81, bass_A, 0])

    # --- FINAL SEQUENCE ---
    out.send_message([0x91, bass_E, 110])
    out.send_message([0x99, 36, 110])     # Big kick for the finish
    out.send_message([0x99, 49, 100])     # Crash Cymbal!
    play_chord(out, chord_C)
    out.send_message([0x81, bass_E, 0])

    out.send_message([0x91, bass_D, 110])
    out.send_message([0x99, 38, 110])     
    play_chord(out, chord_D)
    out.send_message([0x81, bass_D, 0])

    out.send_message([0x91, bass_A, 110])
    out.send_message([0x99, 36, 110])     
    play_chord(out, chord_A7sus4)
    out.send_message([0x81, bass_A, 0])
    
    out.send_message([0x91, bass_A, 110])
    out.send_message([0x99, 36, 110])     
    out.send_message([0x99, 49, 100])     # Crash Cymbal!
    play_chord(out, chord_A7sus4)
    out.send_message([0x81, bass_A, 0])

import rtmidi 
from mido import MidiFile, Message, MidiTrack
from enum import Enum 

class Instrument(Enum):
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

if __name__ == "__main__":
    
    mid = MidiFile('./data/Bohemian_Rhapsody.mid')
    
    # 1. Initialize the new file with the ORIGINAL clock resolution
    mid2 = MidiFile(ticks_per_beat=mid.ticks_per_beat)
    
    # 2. Always copy Track 0 to preserve the tempo and time signatures
    if len(mid.tracks) > 0:
        mid2.tracks.append(mid.tracks[0])

    temp = None # Safely initialize temp

    # 3. Loop through the remaining tracks
    for i, track in enumerate(mid.tracks[1:]): 
        print('Scanning Track {}: {}'.format(i + 1, track.name))
        
        for msg in track:
            if msg.type == 'program_change':
                if msg.program in Instrument.PIANO.value:
                    print('SUCCESS: Found the first PIANO!')
                    temp = track 
                    break # Break the INNER loop
        
        # 4. If we successfully found our piano and assigned it to temp, 
        # break the OUTER loop so we don't overwrite it!
        if temp is not None:
            break 

    # 5. Save the file
    if temp is not None:
        mid2.tracks.append(temp)
        mid2.save('./data/new_song.mid')
        print("File saved as 'new_song.mid'")
    else:
        print("No piano track was found in this file.")
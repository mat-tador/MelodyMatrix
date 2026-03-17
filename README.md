# MelodyMatrix
CSCI 5300 Software Engineering Project

## MIDI Engine 

### Part one: Creating the device 
In order to play a midi file you need a device which is able to do it. Linux does not have it so you can run in the backgroun `fluidsynth`. 
```
sudo apt-get update
sudo apt-get install fluidsynth fluid-soundfont-gm
fluidsynth -a pulseaudio -m alsa_seq -i /usr/share/sounds/sf2/FluidR3_GM.sf2
```
### Part two: Sending message to the device 
MIDI stands for Musical Instrumnet Digital Interface. It is a protocol for electronic music based on messages. The messages are sent to the device. It is possible to play them in the following way: 
```python
import rtmidi 

out = rtmidi.RtMidiOut()
ports = out.get_ports()
print(ports)

out.open_port(1)

message = [0x90, 60, 100]  # Note on: C4, velocity 100
out.send_message(message)

message = [0x80, 60, 0]  # Note off: C4
out.send_message(message)

out.close_port()
```

### Part three: Playing chords 

`MIDI_engine.py` plays the cords of wonderwall. 

## MIDI Parser 

The MIDI parser wants to extract the style of a music instrument from a MIDI file. For this reason the architecture will look like this: 
1. Get MIDI files 
2. Filter instrument 
3. Generate Markov chains 

To do this we will use the `mido` library. 

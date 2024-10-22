import time
from BLE_CEEO import Yell

NoteOn = 0x90
NoteOff = 0x80

# Define MIDI note numbers for melody
notes = {
    'E': 64,
    'D': 62,
    'C': 60,
    'G': 67
}

# Define the melody
melody = [
    'E', 'D', 'C', 'D', 'E', 'E', 'E',
    'D', 'D', 'D', 'E', 'G', 'G',
    'E', 'D', 'C', 'D', 'E', 'E', 'E',
    'E', 'D', 'D', 'E', 'D', 'C'
]

# Define drum notes
drums = {
    'kick': 36,
    'snare': 38,
    'hihat': 42
}

# Velocity
velocity = 64  # Adjust for melody
drum_velocity = 80  # Adjust for drums

p = Yell('Fred', verbose=True, type='midi')
p.connect_up()

melody_channel = 0  # Channel 1 (0 in code)
drum_channel = 9    # Channel 10 (9 in code)

# Function to send MIDI messages
def send_midi(cmd, note, velocity, channel, timestamp):
    payload = bytes([
        (timestamp >> 7 & 0b111111) | 0x80,  # timestamp high
        0x80 | (timestamp & 0b1111111),      # timestamp low
        cmd | (channel & 0x0F),              # Command with channel
        note,                                 # Note number
        velocity                              # Velocity
    ])
    p.send(payload)

# Set note duration
melody_duration = 500  # Milliseconds
drum_duration = 100    # Milliseconds

time.sleep(3)

# Play melody and drum track
for i in range(len(melody)):
    timestamp = time.ticks_ms()

    # Play drum pattern
    if i % 2 == 0:  # Kick on 1 and 3
        send_midi(NoteOn, drums['kick'], drum_velocity, drum_channel, timestamp)
        send_midi(NoteOff, drums['kick'], 0, drum_channel, timestamp + drum_duration)  # Short duration
    if i % 2 == 1:  # Snare on 2 and 4
        send_midi(NoteOn, drums['snare'], drum_velocity, drum_channel, timestamp)
        send_midi(NoteOff, drums['snare'], 0, drum_channel, timestamp + drum_duration)

    # Hi-Hat on every eighth note
    send_midi(NoteOn, drums['hihat'], drum_velocity, drum_channel, timestamp)
    send_midi(NoteOff, drums['hihat'], 0, drum_channel, timestamp + 50)

    # Play melody note
    # Play melody note
    note = melody[i]
    send_midi(NoteOn, notes[note], velocity, melody_channel, timestamp)
    send_midi(NoteOff, notes[note], 0, melody_channel, timestamp + melody_duration)  # Duration of the note

    time.sleep(0.5)  # Adjust for tempo

p.disconnect()

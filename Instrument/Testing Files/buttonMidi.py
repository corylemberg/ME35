import time
from BLE_CEEO import Yell
from machine import Pin, ADC

NoteOn = 0x90
NoteOff = 0x80
StopNotes = 123
SetInstrument = 0xC0
Reset = 0xFF
ControlChange = 0xB0  # Control Change Command

velocity = {'off':0, 'pppp':8,'ppp':20,'pp':31,'p':42,'mp':53,
    'mf':64,'f':80,'ff':96,'fff':112,'ffff':127}

x = Pin('GPIO8', Pin.IN)
y = Pin('GPIO6', Pin.IN)
pot = ADC('GPIO28')

p = Yell('Cory', verbose=True, type='midi')
p.connect_up()

channel = 0
note = 56
cmd = NoteOn
channel = 0x0F & channel
timestamp_ms = time.ticks_ms()
tsM = (timestamp_ms >> 7 & 0b111111) | 0x80
tsL = 0x80 | (timestamp_ms & 0b1111111)
c = cmd | channel

prevX = x.value()
prevY = y.value()
prevPotValue = pot.read_u16()

while True:

    currentPotValue = pot.read_u16()
    
    # Send Control Change for attack level if potentiometer value changed
    if currentPotValue != prevPotValue:
        # Map the potentiometer value to a range suitable for MIDI (0-127)
        mappedValue = int((currentPotValue/65535)*127)
        payload = bytes([tsM, tsL, ControlChange | channel, 1, mappedValue]) # modulation
        # payload = bytes([tsM, tsL, ControlChange | channel, 7, mappedValue]) # volume
        # payload = bytes([tsM, tsL, ControlChange | channel, 64, mappedValue]) # sustain pedal
        # payload = bytes([tsM, tsL, ControlChange | channel, 11, mappedValue])
        p.send(payload)
        prevPotValue = currentPotValue  # Update previous pot value

    if x.value() != prevX:
        if not x.value():
            print("Toggle On")
            payload = bytes([tsM, tsL, cmd | channel, 60, velocity['f']])
            p.send(payload)
        else:
            print("Toggle OFF")
            payload = bytes([tsM, tsL, cmd | channel, 60, velocity['off']])
            p.send(payload)
    
    if y.value() != prevY:
        if not y.value():
            print("Toggle On")
            payload = bytes([tsM, tsL, cmd | 1, 48, velocity['f']])
            p.send(payload)
        else:
            print("Toggle OFF")
            payload = bytes([tsM, tsL, cmd | 1, 48, velocity['off']])
            p.send(payload)

    print(currentPotValue)  # Print current potentiometer value

    prevX = x.value()
    prevY = y.value()

    time.sleep_ms(100)

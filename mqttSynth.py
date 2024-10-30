import time
from BLE_CEEO import Yell
from machine import I2C, Pin, ADC
from Adafruit_Trellis import AdafruitTrellis
import asyncio
import network
from mqtt import MQTTClient

# Midi Constants
NoteOn = 0x90
NoteOff = 0x80
StopNotes = 123
SetInstrument = 0xC0
Reset = 0xFF
ControlChange = 0xB0  # Control Change Command
channel = 0
note = 56
cmd = NoteOn
channel = 0x0F & channel
timestamp_ms = time.ticks_ms()
tsM = (timestamp_ms >> 7 & 0b111111) | 0x80
tsL = 0x80 | (timestamp_ms & 0b1111111)
com = cmd | channel

velocity = {'off':0, 'pppp':8,'ppp':20,'pp':31,'p':42,'mp':53,
    'mf':64,'f':80,'ff':96,'fff':112,'ffff':127}

# bluetooth setup
p = Yell('Cory', verbose=True, type='midi')
p.connect_up()

octave = 0
enable = 0

def internet():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('Wren 540', 'catholicallgirlsschool')

    while wlan.ifconfig()[0] == '0.0.0.0':
        print('.', end=' ')
        time.sleep(1)

    # We should have a valid IP now via DHCP
    print(wlan.ifconfig())

# Callback function for MQTT. Sets global enable
def callback(topic, msg):
    global enable
    command = msg.decode()
    print((topic.decode(), msg.decode()))
    if command == 'on_3':
        enable = True
    if command == 'off_3':
        enable = False

# MQTT initialization and handler function
async def mqtt():
    mqtt_broker = 'broker.emqx.io' 
    port = 1883
    topic_sub = 'ME35-24/Team'

    client = MQTTClient('ME35_cory', mqtt_broker , port, keepalive=60)
    client.connect()
    client.set_callback(callback)          # set the callback if anything is read
    client.subscribe(topic_sub.encode())   # subscribe to a bunch of topics
    
    while True:
        client.check_msg()
        await asyncio.sleep(0.25)

async def slider():
   
    slider = ADC('GPIO26')
    prevSlideValue = slider.read_u16()
    while True:
        currentSlideValue = slider.read_u16()
        
        # Send Control Change for attack level if potentiometer value changed
        if currentSlideValue != prevSlideValue:
            # Map the potentiometer value to a range suitable for MIDI (0-127)
            mappedValue = int((currentSlideValue/65535)*127)
            payload = bytes([tsM, tsL, ControlChange | channel, 7, mappedValue]) # volume
            p.send(payload)
            prevSlideValue = currentSlideValue  # Update previous pot value
        await asyncio.sleep(0.01)

async def knob1():
   
    knob1 = ADC('GPIO27')
    prevKnob1Value = knob1.read_u16()
    while True:
        currentKnob1Value = knob1.read_u16()
        
        # Send Control Change for attack level if potentiometer value changed
        if currentKnob1Value != prevKnob1Value:
            # Map the potentiometer value to a range suitable for MIDI (0-127)
            mappedValue = int((currentKnob1Value/65535)*127)
            payload = bytes([tsM, tsL, ControlChange | channel, 1, mappedValue]) # modulation
            p.send(payload)
            prevKnob1Value = currentKnob1Value  # Update previous pot value
        await asyncio.sleep(0.01)

async def knob2():
    global octave
    knob2 = ADC('GPIO28')
    prevKnob2Value = knob2.read_u16()
    while True:
        currentKnob2Value = knob2.read_u16()
        
        # Send Control Change for attack level if potentiometer value changed
        if currentKnob2Value != prevKnob2Value:
            # Map the potentiometer value to a range suitable for MIDI (0-127)
            mappedValue = int((currentKnob2Value/65535)*8) - 4
            octave = mappedValue * 12
            prevKnob2Value = currentKnob2Value  # Update previous pot value
        await asyncio.sleep(0.01)
    # knob2 = ADC('GPIO28')
    # prevKnob2Value = knob2.read_u16()
    # while True:
    #     currentKnob2Value = knob2.read_u16()
        
    #     # Send Control Change for attack level if potentiometer value changed
    #     if currentKnob2Value != prevKnob2Value:
    #         # Map the potentiometer value to a range suitable for MIDI (0-127)
    #         mappedValue = int((currentKnob2Value/65535)*127)
    #         payload = bytes([tsM, tsL, ControlChange | channel, 71, mappedValue]) # pan
    #         p.send(payload)
    #         prevKnob2Value = currentKnob2Value  # Update previous pot value
    #     await asyncio.sleep(0.01)

async def drumpad():
    # Constants for modes
    MOMENTARY = 0
    LATCHING = 1
    MODE = MOMENTARY  # Set the mode here

    # I2C setup
    i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)  # Adjust pins and frequency

    # Setup for the Trellis
    matrix0 = AdafruitTrellis(i2c=i2c)
    trellis = matrix0  # Just using one for now
    NUMTRELLIS = 1
    numKeys = NUMTRELLIS * 16

    # Initialize the trellis
    trellis.begin()

    DRUMS = {
        0: 46,
        1: 41,
        2: 42,
        3: 43,
        4: 38,
        5: 45,
        6: 47,
        7: 35,
        8: 51,
        9: 57,
        10: 59,
        11: 65,
        12: 62,
        13: 49,
        14: 63,
        15: 54
    }

    # trellis.displaybuffer = bytearray(0x00 *16)
    # trellis.write_display()

    while True:
        if trellis.read_switches():
            # print("Keys State:", trellis.keys)
            for i in range(numKeys):
                if MODE == MOMENTARY:
                    if trellis.just_pressed(i):
                        print(f"Button {i} pressed")
                        payload = bytes([tsM, tsL, cmd | 1, DRUMS[i], velocity['f']])
                        p.send(payload)
                        trellis.set_led(i)
                    if trellis.just_released(i):
                        print(f"Button {i} released")
                        payload = bytes([tsM, tsL, cmd | 1, DRUMS[i], velocity['off']])
                        p.send(payload)
                        trellis.clr_led(i)

                elif MODE == LATCHING:
                    if trellis.just_pressed(i):
                        print(f"Button {i} pressed")
                        if trellis.is_key_pressed(i):
                            trellis.clr_led(i)
                        else:
                            trellis.set_led(i)

            trellis.write_display()
        await asyncio.sleep(0.03)  # 30ms delay

async def piano():
    keys = {
        'C': Pin('GPIO13', Pin.IN),
        'C#': Pin('GPIO12', Pin.IN),
        'D': Pin('GPIO11', Pin.IN),
        'D#': Pin('GPIO10', Pin.IN),
        'E': Pin('GPIO9', Pin.IN),
        'F': Pin('GPIO8', Pin.IN),
        'F#': Pin('GPIO7', Pin.IN),
        'G': Pin('GPIO6', Pin.IN),
        'G#': Pin('GPIO5', Pin.IN),
        'A': Pin('GPIO4', Pin.IN),
        'A#': Pin('GPIO3', Pin.IN),
        'B': Pin('GPIO2', Pin.IN)
    }

    # Store previous states of keys
    prev_states = {key: pin.value() for key, pin in keys.items()}
    active_notes = set()  # Track currently active notes

    while True:
        if enable:    
            for key, pin in keys.items():
                current_value = pin.value()
                note_number = {
                    'C': 60, 'C#': 61, 'D': 62, 'D#': 63,
                    'E': 64, 'F': 65, 'F#': 66, 'G': 67,
                    'G#': 68, 'A': 69, 'A#': 70, 'B': 71
                }[key]

                if current_value != prev_states[key]:
                    if not current_value:  # Key pressed
                        print(f"{key} Toggle On")
                        active_notes.add(note_number)  # Add note to active set
                        payload = bytes([tsM, tsL, com, note_number + octave, velocity['f']])
                        p.send(payload)
                    else:  # Key released
                        print(f"{key} Toggle OFF")
                        if note_number in active_notes:  # Ensure the note is active
                            active_notes.remove(note_number)  # Remove note from active set
                            payload = bytes([tsM, tsL, com, note_number + octave, velocity['off']])
                            p.send(payload)

                    # Update previous state
                    prev_states[key] = current_value

            await asyncio.sleep(0.01)


async def main():
    asyncio.create_task(drumpad())
    asyncio.create_task(slider())
    asyncio.create_task(knob1())
    asyncio.create_task(knob2())
    asyncio.create_task(piano())
    internet()
    p.send(bytes([tsM, tsL, 0xB0, 0x7B, 0x00])) # turn all notes off

    while True:
        await asyncio.sleep(0.01)

asyncio.run(main())
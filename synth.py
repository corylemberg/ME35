import time
from BLE_CEEO import Yell
from machine import I2C, Pin, ADC
from Adafruit_Trellis import AdafruitTrellis
import asyncio

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
c = cmd | channel

velocity = {'off':0, 'pppp':8,'ppp':20,'pp':31,'p':42,'mp':53,
    'mf':64,'f':80,'ff':96,'fff':112,'ffff':127}

# bluetooth setup
p = Yell('Cory', verbose=True, type='midi')
p.connect_up()

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
    x = Pin('GPIO8', Pin.IN)
    y = Pin('GPIO6', Pin.IN)
    prevX = x.value()
    prevY = y.value()

    while True:
        if x.value() != prevX:
            if not x.value():
                print("Toggle On")
                payload = bytes([tsM, tsL, c, 60, velocity['f']])
                p.send(payload)
            else:
                print("Toggle OFF")
                payload = bytes([tsM, tsL, c, 60, velocity['off']])
                p.send(payload)
    
        if y.value() != prevY:
            if not y.value():
                print("Toggle On")
                payload = bytes([tsM, tsL, c, 48, velocity['f']])
                p.send(payload)
            else:
                print("Toggle OFF")
                payload = bytes([tsM, tsL, c, 48, velocity['off']])
                p.send(payload)

        prevX = x.value()
        prevY = y.value()

        await asyncio.sleep(0.01)

async def main():
    asyncio.create_task(drumpad())
    asyncio.create_task(piano())

    while True:
        await asyncio.sleep(0.01)

asyncio.run(main())
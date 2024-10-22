from machine import I2C, Pin
import time
from Adafruit_Trellis import AdafruitTrellis

# Constants for modes
MOMENTARY = 0
LATCHING = 1
MODE = LATCHING  # Set the mode here

# I2C setup
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)  # Adjust pins and frequency

# Setup for the Trellis
matrix0 = AdafruitTrellis(i2c=i2c)
trellis = matrix0  # Just using one for now
NUMTRELLIS = 1
numKeys = NUMTRELLIS * 16

# Initialize the trellis
trellis.begin()

# Light up all the LEDs in order
for i in range(numKeys):
    trellis.set_led(i)
    trellis.write_display()
    time.sleep(0.05)

# Turn them off
for i in range(numKeys):
    trellis.clr_led(i)
    trellis.write_display()
    time.sleep(0.05)

# Main loop
while True:
    time.sleep(0.03)  # 30ms delay

    if trellis.read_switches():
        # print("Keys State:", trellis.keys)
        for i in range(numKeys):
            if MODE == MOMENTARY:
                if trellis.just_pressed(i):
                    print(f"Button {i} pressed")
                    trellis.set_led(i)
                if trellis.just_released(i):
                    print(f"Button {i} released")
                    trellis.clr_led(i)

            elif MODE == LATCHING:
                if trellis.just_pressed(i):
                    print(f"Button {i} pressed")
                    if trellis.is_key_pressed(i):
                        trellis.clr_led(i)
                    else:
                        trellis.set_led(i)

        trellis.write_display()

import neopixel
from machine import Pin
import time

led = neopixel.NeoPixel(Pin(28),1)

while True:
    for i in range(255):
        led[0] = (i, 0, 0)
        # led[0] = (0, i, 0)
        led.write()
        time.sleep(0.01)

    for i in range(255, 0, -1):
        led[0] = (i, 0, 0)
        # led[0] = (0, i, 0)
        led.write()
        time.sleep(0.01)
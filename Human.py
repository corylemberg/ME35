import asyncio
import neopixel
from machine import Pin, PWM

class Human:
    def __init__(self, zombie = 0, ID = 0):
        self.zombie = zombie
        self.ID = ID
        self.counter = 0.0
        self.state = [0] * 13
        self.led = neopixel.NeoPixel(Pin(28),1)
        self.buzzer = PWM(Pin('GPIO18', Pin.OUT))
        self.buzzer.freq(260)
    
    def check_health(self):
        for i in range(len(self.state)):
            if self.state[i] >= 3:
                self.zombie = 1
                self.ID = i + 1
                break

    async def light(self):
        while True:
            for i in range(255):
                if not self.zombie:
                    self.led[0] = (0, i, 0)
                elif self.zombie:
                    self.led[0] = (i, 0, 0)
                self.led.write()
                await asyncio.sleep(0.01)

            for i in range(255, 0, -1):
                if not self.zombie:
                    self.led[0] = (0, i, 0)
                elif self.zombie:
                    self.led[0] = (i, 0, 0)
                self.led.write()
                await asyncio.sleep(0.01)
            await asyncio.sleep(0)

    async def buzz(self):
        while True:
            while self.zombie:
                self.buzzer.freq(220)
                self.buzzer.duty_u16(10000)
            await asyncio.sleep(0.1)
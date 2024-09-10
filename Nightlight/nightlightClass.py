# buttonPin is GPIO20
# blueLEDPin is GPIO1
# buzzerPin is GPIO18

from machine import Pin, PWM
import uasyncio as asyncio
import random
import neopixel


class Nightlight:
    def __init__(self, buttonPin, blueLEDPin, buzzerPin):

        self.button = Pin(buttonPin, Pin.IN)
        self.bLED = PWM(Pin(blueLEDPin, Pin.OUT))
        self.bLED.freq(1000)
        self.buzz = PWM(Pin(buzzerPin, Pin.OUT))
        self.buzz.freq(440)
        self.led = neopixel.NeoPixel(Pin(28),1)

    buzzOn = False

    def changeColor(self):
        newColor = [0, 0, 0]
        newColor[0] = random.randint(0, 127)
        newColor[1] = random.randint(0, 127)
        newColor[2] = random.randint(0, 127)

        self.led[0] = newColor
        self.led.write()
    
    async def breathe(self):
        RATE = 1000
        count = 1
        i = RATE

        while True:

            if i >= 65535:
                count = 0
            elif i <= 0:
                count = 1

            if count == 1:
                i = i + RATE
            elif count == 0:
                i = i - RATE
            
            self.bLED.duty_u16(i)
            await asyncio.sleep(0.05)
    
    async def check_button_status(self):
        while True:
            if self.button.value() == 0:
                print("button pressed")
                self.changeColor()
                self.buzzOn = True
                await asyncio.sleep(1)
            await asyncio.sleep(0.01)

    async def buzzer(self):
        while True:    
            if self.buzzOn:    
                self.buzz.duty_u16(500)
                await asyncio.sleep(0.5)
                self.buzz.duty_u16(0)
                self.buzzOn = False
            await asyncio.sleep(0.1)

async def main():
    nightlight = Nightlight('GPIO20', 'GPIO1', 'GPIO18')
    asyncio.create_task(nightlight.breathe())
    asyncio.create_task(nightlight.check_button_status())
    asyncio.create_task(nightlight.buzzer())
    while True:
        await asyncio.sleep(0.1)

asyncio.run(main())
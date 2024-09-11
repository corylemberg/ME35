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

        self.enable = False
        self.buzzOn = False
        self.neoOn = False
        self.currentColor = [0, 10, 5]

    def changeColor(self):
        # newColor = [0, 0, 0]
        # newColor[0] = random.randint(0, 127)
        # newColor[1] = random.randint(0, 127)
        # newColor[2] = random.randint(0, 127)
        prevColor = self.currentColor
        colorList = [[10, 0, 0], [10, 2, 0], [10, 5, 0], 
                     [0, 10, 0], [0, 10, 5], [0, 3, 10],
                     [5, 0, 10], [10, 5, 2], [10, 10, 10]]
        newColor = colorList[random.randint(0, 8)]
        while True:
            if newColor == prevColor:
                newColor = colorList[random.randint(0, 8)]
            else:
                break
        print(newColor)
        self.currentColor = newColor
    
    async def breathe(self):
        RATE = 1000
        count = 1
        i = RATE

        while True:
            if self.enable:
                if i >= 65535:
                    count = 0
                elif i <= 0:
                    count = 1

                if count == 1:
                    i = i + RATE
                elif count == 0:
                    i = i - RATE
            
                self.bLED.duty_u16(i)
            else:
                self.bLED.duty_u16(0)

            await asyncio.sleep(0.01)
    
    async def check_button_status(self):
        while True:
            if self.enable:
                self.neoOn = True
                if self.button.value() == 0:
                    # the button is being pressed
                    self.changeColor()
                    self.buzzOn = True
                    await asyncio.sleep(1)
            else:
                self.neoOn = False
            await asyncio.sleep(0.01)

    async def neo(self):
        while True:
            if self.neoOn:
                self.led[0] = self.currentColor
            else:
                self.led[0] = (0, 0, 0)
            self.led.write()
            await asyncio.sleep(0.01)

    async def buzzer(self):
        while True:
            if self.enable:    
                if self.buzzOn:    
                    self.buzz.duty_u16(500)
                    await asyncio.sleep(0.5)
                    self.buzz.duty_u16(0)
                    self.buzzOn = False
                else:
                    self.buzz.duty_u16(0)
            await asyncio.sleep(0.01)
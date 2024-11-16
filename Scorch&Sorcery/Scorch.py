import asyncio, neopixel, time
from machine import Pin
import time
from networking import Networking

RED = (100, 0, 0)
ORANGE = (100, 65, 0)
BLUE = (0, 0, 100)
WHITE = (100, 100, 100)
GREEN = (0, 128, 0)
OFF = (0, 0, 0)

#Initialise
networking = Networking()
recipient_mac = b'\xFF\xFF\xFF\xFF\xFF\xFF' #This mac sends to all

class Dragon:
    def __init__(self):
        self.button = Pin('GPIO20', Pin.IN)
        self.led = neopixel.NeoPixel(Pin(28),1)
        self.cooldown = 0
        self.totalGametime = 600 #10 minute timer 
        self.scorched = False #Boolean when all wizards have been scorched
        self.wizardID = [0] * 13

    def receive(self):
        print("Receive")

    async def listen_ID(self):

        players = 0x0

        #Check ID numbers
        lastmsg = str(networking.aen.irq(self.receive))
        #convert lastmsg to just the id number
        idnumber = ''

        if idnumber.isdigit():
            players = players | (1 << int(idnumber))
            if players == 0xF:
                self.scorched = True

        #Add ID number to array

    async def breath_fire(self):
        prevButton = 0
        message =  'breathingFire'
        while True:
            # Conditional to Breath Fire if button is pressed and not on cooldown
            if self.button != prevButton and prevButton and not self.cooldown:
                networking.aen.send(recipient_mac, message)
                self.cooldown = 1
            prevButton = self.button
            await asyncio.sleep(0.05)

    async def manage_fire(self):
        while True:
            # Begin 15 second cooldown
            if self.cooldown:
                await asyncio.sleep(15)
                self.cooldown = 0

    async def neoPixel(self):
        while True:
            
            # Blink orange to indicate cooldown
            if self.cooldown:
                self.led[0] = ORANGE
                await asyncio.sleep(0.25)
                self.led[0] = OFF
                await asyncio.sleep(0.25)

            # Show white to indicate game in progress
            self.led[0] = WHITE
            await asyncio.sleep(0)
    
    async def timer(self):
        #Timer decrementing till 10 minutes has gone by
        while self.totalGametime > 0:
            minutes, seconds = divmod(self.totalGametime, 60)
            print(f"Time remaining: {minutes:02d}:{seconds:02d}", end='\r')
            await asyncio.sleep(.1)
            self.totalGametime -= 1

    async def gameOver(self):
        while True:
            if self.scorched:
                self.led[0] = GREEN #Scorch tagged everyone else
            elif self.totalGametime == 0:
                self.led[0] = RED #Wizards outlasted the timer
            await asyncio.sleep(.01)

    async def main(self):

        task1 = self.breath_fire()
        task2 = self.manage_fire()
        task3 = self.neoPixel()
        task4 = self.timer()
        task5 = self.gameOver()

        asyncio.gather(task1, task2, task3, task4, task5)




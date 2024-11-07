import asyncio, neopixel, time
from machine import Pin
from Tufts_ble import Yell, Sniff

RED = (100, 0, 0)
ORANGE = (100, 65, 0)
BLUE = (0, 0, 100)
WHITE = (100, 100, 100)
GREEN = (0, 128, 0)
OFF = (0, 0, 0)

class Dragon:
    def __init__(self):
        self.button = Pin('GPIO20', Pin.IN)
        self.led = neopixel.NeoPixel(Pin(28),1)
        self.cooldown = 0
        self.totalGametime = 600 #10 minute timer 
        self.scorched = False #Boolean when all wizards have been scorched
        self.wizardID = [0] * 13

    async def listen_ID(self):
        c = Sniff('!', verbose = True)
        c.scan(0) #scan forever
        #Check ID numbers
        #Add ID number to array
        



    async def breath_fire(self):
        p = Yell()
        prevButton = 0
        while True:
            
            # Conditional to Breath Fire if button is pressed and not on cooldown
            if self.button != prevButton and prevButton and not self.cooldown:
                #send out BLE
                p.advertise(f'!roar')
                await asyncio.sleep(0.1)
                p.stop_advertising()
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

        if self.totalGametime == 0:
            self.led[0] = RED #Wizards outlasted the timer
            await asyncio.sleep(.01)

    async def allScorched(self):
        #All wizards have been scorched Dragon Wins
        #Check if all IDs have been collected
        if self.scorched == True:
            self.led[0] = GREEN
            await asyncio.sleep(.01)

    async def main(self):

        task1 = self.breath_fire()
        task2 = self.manage_fire()
        task3 = self.neoPixel()
        task4 = self.timer()
        task5 = self.gameOver()
        task6 = self.allScorched()

        asyncio.gather(task1, task2, task3, task4, task5, task6)




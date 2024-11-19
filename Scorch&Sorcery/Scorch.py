import asyncio, neopixel, time
from machine import Pin
import time
from networking import Networking

class Dragon:
    def __init__(self, playerCount = 1):
        self.button = Pin(18, Pin.IN)
        # self.led = neopixel.NeoPixel(Pin(28),1)
        self.cooldown = 0
        self.totalGametime = 300 #5 minute timer 
        self.scorched = False #Boolean when all wizards have been scorched
        self.wizards = {
        }
        self.incomingMac = b'\x00\x00\x00\x00\x00\x00'
        self.playerCount = playerCount

        #Initialise ESPNOW
        self.networking = Networking()
        self.recipient_mac = b'\xFF\xFF\xFF\xFF\xFF\xFF' #This mac sends to all

    def receive(self):
        print("Receive")
        for mac, message, rtime in self.networking.aen.return_messages(): #You can directly iterate over the function
            self.incomingMac = mac

    async def listen_ID(self):
        while True:
            if self.scorched:
                break

            # Receive Wizard Mac Address
            self.networking.aen.irq(self.receive())
            if self.incomingMac != None:
                print("Adding Wizard Mac To Dictionary")
                self.wizards[self.incomingMac] = 1

            # Check if all wizards are hit
            if len(self.wizards) == self.playerCount:
                print("All Wizards Scorched!")
                self.scorched = True

            await asyncio.sleep(0.1)

    async def breath_fire(self):
        prevButton = 0
        message = 'breathingFire'
        while True:
            # Conditional to Breath Fire if button is pressed and not on cooldown
            if self.button != prevButton and prevButton and not self.cooldown:
                self.networking.aen.send(self.recipient_mac, message)
                print("DragonBreath Sent to Wizard")
                self.cooldown = 1
            prevButton = self.button.value()
            await asyncio.sleep(0.05)

    async def manage_fire(self):
        while True:
            # Begin 15 second cooldown
            if self.cooldown:
                print("Dragon Cooling Down")
                await asyncio.sleep(15) 
                self.cooldown = 0
            await asyncio.sleep(0.01)

    # async def neoPixel(self):
    #     while True:
    #         # Blink orange to indicate cooldown
    #         if self.cooldown:
    #             self.led[0] = ORANGE
    #             await asyncio.sleep(0.25)
    #             self.led[0] = OFF
    #             await asyncio.sleep(0.25)

    #         # Show white to indicate game in progress
    #         self.led[0] = WHITE
    #         await asyncio.sleep(0)
    
    async def timer(self):
        while True:    
            #Timer decrementing till 5 minutes has gone by
            if self.totalGametime > 0:
                minutes, seconds = divmod(self.totalGametime, 60)
                print(f"Time remaining: {minutes:02d}:{seconds:02d}", end='\r')
                await asyncio.sleep(1)
                self.totalGametime -= 1

    async def gameOver(self):
        while True:
            if self.scorched:
                # self.led[0] = GREEN #Scorch tagged everyone else
                print("The Dragon wins!")
            elif self.totalGametime == 0:
                # self.led[0] = RED #Wizards outlasted the timer
                print("The Wizards wins!")
            await asyncio.sleep(.01)

    

    async def main(self):
        
        asyncio.create_task(self.breath_fire())
        asyncio.create_task(self.manage_fire())
        asyncio.create_task(self.timer())
        asyncio.create_task(self.gameOver())

        while True:
            await asyncio.sleep(0.1)

dragon = Dragon()    
asyncio.run(dragon.main())

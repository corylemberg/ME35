import asyncio, neopixel, time
from machine import Pin
import time
from networking import Networking

class Dragon:
    def __init__(self, playerCount = 3):
        self.button = Pin(18, Pin.IN)
        self.GREEN = Pin(17,Pin.OUT) #Pin number will be determined later placeholder
        self.RED = Pin(20,Pin.OUT) #Pin number will be determined later placeholder
        self.WHITE = Pin(19, Pin.OUT) #Pin number will be determined later placeholder

        self.cooldown = 0
        self.totalGametime = 300 #5 minute timer
        self.playerCount = playerCount
        self.scorched = False #Boolean when all wizards have been scorched
        self.wizards = {
        }
        self.inGame = False

        #Initialise ESPNOW
        self.msg = ''
        self.incomingMac = b'\x00\x00\x00\x00\x00\x00'
        self.networking = Networking()
        self.recipient_mac = b'\xFF\xFF\xFF\xFF\xFF\xFF' #This mac sends to all
    
    def reset(self):
        print("Reset Func")

    def receive(self):
        # print("Receive")
        for mac, message, rtime in self.networking.aen.return_messages(): #You can directly iterate over the function
            self.incomingMac = mac
            self.msg = message

    async def listen_ID(self):
        while True:
            
            # If reset, set all values back to 0
            if self.msg == '!reset':
                self.inGame = True
                self.scorched = False
                self.cooldown = 0
                self.totalGametime = 300 #5 minute timer 
                self.wizards = {
                }
                self.msg = ''
                self.incomingMac = b'\x00\x00\x00\x00\x00\x00'
                self.RED.off()
                self.GREEN.off()
                self.WHITE.off()
            
            ##################### GAME LOGIC #####################
            # Receive Wizard Macs Address
            self.networking.aen._irq(self.receive())

            if self.scorched:
                continue

            if self.inGame:            
                if self.incomingMac != None and self.incomingMac != b'd\xe83\x874\x1c':
                    print("Adding Wizard Mac To Dictionary")
                    self.wizards[self.incomingMac] = 1

                # Check if all wizards are hit
                if len(self.wizards) == self.playerCount:
                    print("All Wizards Scorched!")
                    self.scorched = True
            ######################################################

            await asyncio.sleep(0.1)

    async def breath_fire(self):
        prevButton = 1
        message = 'breathingFire'
        while True:
            if self.inGame:
                # Conditional to Breath Fire if button is pressed and not on cooldown
                #print("Button not pressed")
                if self.button.value() == 1 and not prevButton and not self.cooldown:
                    self.networking.aen.send(self.recipient_mac, message)
                    print("DragonBreath Sent to Wizard")
                    self.cooldown = 1
                prevButton = self.button.value()
            await asyncio.sleep(0.05)

    async def manage_fire(self):
        while True:
            # Begin 15 second cooldown
            if self.cooldown and self.inGame:
                print("Dragon Cooling Down")
                await asyncio.sleep(15) 
                print("Cooldown Finished")
                self.cooldown = 0
            await asyncio.sleep(0.01)

    async def gameProgress(self):
        while True:
            if self.inGame:
                # Blink Red to indicate cooldown
                if self.cooldown:
                    self.RED.on()
                    await asyncio.sleep(0.25)
                    self.RED.off()
                    await asyncio.sleep(0.25)

                # Show white to indicate game in progress
                self.WHITE.on()
            elif not self.scorched and self.totalGametime != 0:
                # While waiting to start game, flash LEDs
                self.WHITE.off()
                self.RED.on()
                await asyncio.sleep(0.1)
                self.RED.off()
                self.GREEN.on()
                await asyncio.sleep(0.1)
                self.GREEN.off()
                self.WHITE.on()
                await asyncio.sleep(0.1)

            await asyncio.sleep(0.01)
    
    async def timer(self):
        #Timer decrementing till 5 minutes has gone by
        while True:
            if self.totalGametime > 0 and self.inGame:
                minutes, seconds = divmod(self.totalGametime, 60)
                print(f"Time remaining: {minutes:02d}:{seconds:02d}", end='\r')
                self.totalGametime -= 1
                await asyncio.sleep(1)
            await asyncio.sleep(0.01)

    async def gameOver(self):
        while True:
            if self.scorched:
                self.WHITE.off()
                self.RED.off()
                self.GREEN.on() #Scorch tagged everyone else
                self.inGame = False
                print("The Dragon wins!")
            elif self.totalGametime == 0:
                # self.led[0] = RED #Wizards outlasted the timer
                self.WHITE.off()
                self.RED.on()
                self.inGame = False
                print("The Wizards wins!")
            await asyncio.sleep(0.01)
                


    async def main(self):
        
        asyncio.create_task(self.breath_fire())
        asyncio.create_task(self.manage_fire())
        asyncio.create_task(self.listen_ID())
        asyncio.create_task(self.timer())
        asyncio.create_task(self.gameOver())
        asyncio.create_task(self.gameProgress())

        while True:
            # print(f'In the Game: {self.inGame}    ', end='\r')
            await asyncio.sleep(0.01)

dragon = Dragon(playerCount=2)
asyncio.run(dragon.main())
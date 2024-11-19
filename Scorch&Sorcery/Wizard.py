import asyncio
import neopixel
from machine import Pin, PWM
import time
from networking import Networking

class Wizard:
    def __init__(self):
        # self.led = neopixel.NeoPixel(Pin(28),1)
        self.hit = 0
        self.msg = ''
        
        #Initialise ESPNOW
        self.networking = Networking()
        self.recipient_mac = b'\xFF\xFF\xFF\xFF\xFF\xFF'
        

    '''
    Handler function for ESPNOW. Extracts message and stores it in class variable
    '''
    def receive(self):
        # print("Receive")
        for mac, message, rtime in self.networking.aen.return_messages(): #You can directly iterate over the function
            self.msg = message
    
    '''
    Function to handle Wizard health. Each wizard has 1 life. If they are hit
    once they will "die" and not be in the game anymore. Hits are determined based
    on proximity to the Dragon.
    '''
    async def check_health(self):
        while True:
            # Read from ESPNOW
            self.networking.aen.irq(self.receive())
            placeholder = self.networking.aen.rssi()

            try:
                # rssi_value = placeholder[b'T2\x043H\x14'][0] #Cory ESP As Dragon
                rssi_value = placeholder[b'T2\x04!a\x9c'][0] #Jaylen ESP As Dragon
            except KeyError:
                pass

            # if message is detected AND rssi is within the threashold, player gets hit
            if self.msg == 'breathingFire' and rssi_value > -70:
                self.hit = 1

            # If a player is dead, advertise their ID, if not, put them in jail
            if self.hit == 1:
                message =  f'im dead'
                self.networking.aen.send(self.recipient_mac, message)
                print(f'Wizard Is Dead', end='\r')
            else:
                print(f'Wizard Is Alive', end='\r')

            await asyncio.sleep(0.1)
            
    '''
    Function to handle the LED state:
        Dead: Neopixel Off
        Alive: Solid White
    '''
    # async def neoPixel(self):
    #     while True:
    #         # Wizard Dead (Neo Off)
    #         if self.hit == 1:
    #             self.led[0] = OFF
    #         # Wizard in Game (White)
    #         else:
    #             self.led[0] = WHITE

    #         await asyncio.sleep(0)
    
    async def main(self):
        asyncio.create_task(self.check_health())
        while True:
            await asyncio.sleep(0.1)

wizard = Wizard()
asyncio.run(wizard.main())
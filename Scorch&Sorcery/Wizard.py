import asyncio
import neopixel
from machine import Pin, PWM
from Tufts_ble import Sniff, Yell

RED = (100, 0, 0)
BLUE = (0, 0, 100)
WHITE = (100, 100, 100)
OFF = (0, 0, 0)

class Wizard:
    def __init__(self, ID):
        self.ID = ID
        self.timeFirstHit = 0
        self.hitCounter = 0
        self.timeLastHit = 0
        self.led = neopixel.NeoPixel(Pin(28),1)
        self.hit = 0
        self.lives = 2
        self.inJail = 0

    '''
    Function to handle Wizard health. Each wizard has 2 lives. If they are hit
    once they will go to jail for 30 seconds. If they are hit a second time,
    they will "die" and not be in the game anymore. Hits are determined based
    on proximity to the Dragon.
    '''
    async def check_health(self):
        c = Sniff('!', verbose = True)
        c.scan(0)   # 0ms = scans forever
        p = Yell()
        while True:

            # Read message if the player has lives
            if self.lives != 0:
                latest = c.last
                if latest:
                    c.last='' # clear the flag for the next advertisement
                    message = latest[1:]
                    if message == 'roar':
                        self.hit = 1
                        self.lives -= 1

            # If a player is dead, advertise their ID, if not, put them in jail
            if self.lives == 0:
                p.advertise(f'!{self.ID}')
            elif self.hit:
                self.inJail = 1
                await asyncio.sleep(30)
                self.inJail = 0
                self.hit = 0
            
            await asyncio.sleep(0.1)

            
    '''
    Function to handle the neopixel state:
        Dead: Neopixel Off
        Jail: Blink Red
        Alive: Solid White
    '''
    async def neoPixel(self):
        while True:
            # Wizard Dead (Neo Off)
            if self.lives == 0:
                self.led[0] = OFF
            # Wizard in Jail (Blink Red)
            elif self.inJail:
                self.led[0] = RED
                await asyncio.sleep(0.5)
                self.led[0] = OFF
                await asyncio.sleep(0.5)
            # Wizard in Game (White)
            else:
                self.led[0] = WHITE

            await asyncio.sleep(0)
                
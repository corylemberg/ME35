# Inferno Chase
# ME35 Final Project
# Jaylen and Cory
# Description:  One dragon will chase everyone else attempting to tag them
#               by being in range of BLE. Once tagged, the players will go
#               to jail and need to wait 30 seconds before they can respawn.
#               If you get tagged twice, you are out of the game. The game will
#               last 10 min and if there are any wizards remaining at the end, they
#               win.


import time
from Tufts_ble import Sniff, Yell
from Wizard import Wizard
import asyncio
from machine import Pin, PWM

class Inferno_Chase:

    def __init__(self):
        
        self.THREASHOLD = -60
        self.sorcer = Wizard(scorch = 0, ID = 0)
        self.c = Sniff('!', verbose = True) 
        self.timer = 600000 #10 minute timer
        self.fireBreath = Yell()
        self.fireButton = Pin(4, Pin.IN, Pin.PULL_UP)
        self.delayFire = 15000 # delay fire for 15 seconds after button pressed
        self.fireStatus = True
        

    async def fire(self):

        if self.fireStatus == True:
            if self.fireButton == 1:
                self.fireBreath.advertise()
                await asyncio.sleep(.1)
                self.fireBreath.stop_advertising()

    async def fireDelay(self):

        if self.fireButton == 1:
            self.fireStatus = False
            



        


        




    


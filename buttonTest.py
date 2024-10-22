import time
from machine import Pin

x = Pin('GPIO8', Pin.IN)
y = Pin('GPIO6', Pin.IN)

prevX = x.value()
prevY = y.value()

while True:

    if x.value() != prevX:
        if not x.value():
            print("Button 1 On")
        else:
            print("Button 1 Off")
    
    if y.value() != prevY:
        if not y.value():
            print("Toggle 2 On")
        else:
            print("Toggle 2 OFF")
            
    prevX = x.value()
    prevY = y.value()

    time.sleep_ms(100)

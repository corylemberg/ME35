from machine import Pin
import time

def snake():

    l0 = Pin('GPIO0', Pin.OUT)
    l1 = Pin('GPIO1', Pin.OUT)
    l2 = Pin('GPIO2', Pin.OUT)
    l3 = Pin('GPIO3', Pin.OUT)
    l4 = Pin('GPIO4', Pin.OUT)
    l5 = Pin('GPIO5', Pin.OUT)

    LEDs = [l0, l1, l2, l3, l4, l5]
    DELs = LEDs[::-1]
    while True:
        for i in LEDs:
            i.on()
            time.sleep(0.01)
            i.off()
            time.sleep(0.01)
        for i in DELs:
            i.on()
            time.sleep(0.01)
            i.off()
            time.sleep(0.01)

snake()
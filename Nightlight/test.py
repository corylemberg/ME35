from machine import PWM, Pin
import time

buzz = PWM(Pin(0, Pin.OUT))

buzz.freq(1000)

buzz.duty_u16(20000)
time.sleep(1)
buzz.duty_u16(0)
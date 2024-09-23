import time
from Tufts_ble import Yell

while True:
    p = Yell()
    p.advertise(f'!4')
    p.advertise(f'!3')
    time.sleep(0.1)
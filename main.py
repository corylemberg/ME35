import time
from Tufts_ble import Sniff, Yell
from Human import Human
import asyncio

THREASHOLD = -60
john = Human(zombie=1, ID=5)

c = Sniff('!', verbose = True)
c.scan(0)   # 0ms = scans forever 

async def run():
    global THREASHOLD
    '''
    Loop for Human. Checks for messages from zombies and updates status
    in the human class.
    '''
    while not john.zombie:
        john.check_health()
        latest = c.last
        print(c.rssi)
        if latest:
            c.last='' # clear the flag for the next advertisement
            if latest[1:].isdigit() :  # Count only if number
                if c.rssi > THREASHOLD:
                    message = int(latest[1:])
                    john.state[message - 1] += 1
            # else:
            #     print("not a number")
        print(john.counter)
        await asyncio.sleep(0.1)

    '''
    Loop for Zombie. Broadcasts the zombie ID number.
    '''
    p = Yell()
    print(f'Zombie: {john.ID}')
    while john.zombie:
        p.advertise(f'!{john.ID}')
        await asyncio.sleep(0.1)
        p.stop_advertising()

async def main():
    asyncio.create_task(run())
    asyncio.create_task(john.light())
    # asyncio.create_task(john.buzz())
    while True:
        await asyncio.sleep(0.1)
    
asyncio.run(main())
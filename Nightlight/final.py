from Nightlight import Nightlight
import uasyncio as asyncio
import network
import time
from mqtt import MQTTClient

enable = False

def internet():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('Wren 540', 'catholicallgirlsschool')

    while wlan.ifconfig()[0] == '0.0.0.0':
        print('.', end=' ')
        time.sleep(1)

    # We should have a valid IP now via DHCP
    print(wlan.ifconfig())

def callback(topic, msg):
    global enable
    command = msg.decode()
    print((topic.decode(), msg.decode()))
    if command == 'start':
        enable = True
    if command == 'end':
        enable = False

async def mqtt():
    mqtt_broker = 'broker.hivemq.com' 
    port = 1883
    topic_sub = 'ME35-24/MedhaAndCory'
    topic_pub = 'ME35-24/Rex'

    client = MQTTClient('ME35_cory', mqtt_broker , port, keepalive=60)
    client.connect()
    client.set_callback(callback)          # set the callback if anything is read
    client.subscribe(topic_sub.encode())   # subscribe to a bunch of topics
    
    msg = 'working...'
    i = 0
    while True:
        i+=1
        if i %5 == 0:
            client.publish(topic_pub.encode(),msg.encode())
        client.check_msg()
        await asyncio.sleep(1)

async def main():
    global enable
    asyncio.create_task(mqtt())
    nightlight = Nightlight('GPIO20', 'GPIO1', 'GPIO18')
    asyncio.create_task(nightlight.breathe())
    asyncio.create_task(nightlight.check_button_status())
    asyncio.create_task(nightlight.neo())
    asyncio.create_task(nightlight.buzzer())
    while True:
        nightlight.enable = enable
        await asyncio.sleep(0.1)

internet()
asyncio.run(main())
import time
import network
from mqtt import MQTTClient
import sensor
import math

################ INTERNET AND MQTT SETUP ################
SSID = "Tufts_Robot"  # Network SSID
KEY = ""  # Network key

# Init wlan module and connect to network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, KEY)

while not wlan.isconnected():
    print('Trying to connect to "{:s}"...'.format(SSID))
    time.sleep_ms(1000)

# We should have a valid IP now via DHCP
print("WiFi Connected ", wlan.ifconfig())

client = MQTTClient("ME35-24", "broker.hivemq.com", port=1883)
client.connect()
########################################################

##################### Camera Setup #####################
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()
########################################################

currentTag = ''
    
while True:
    
    clock.tick()
    img = sensor.snapshot()
    for tag in img.find_apriltags():
        img.draw_rectangle(tag.rect(), color=(255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color=(0, 255, 0))
        
        # Ensure we have the right attributes for the tag
        tag_id = tag.id()
        tag_name = tag.family()  # Use the correct method to get tag family
        tag_rotation = (180 * tag.rotation()) / math.pi
        
        currentTag = f'{tag_id}, {tag_name}'

        print("Tag Family %s, Tag ID %d, rotation %f (degrees)" % (tag_name, tag_id, tag_rotation))

    if currentTag == f'42, 16':
        client.publish("ME35-24/kai", str(tag_rotation))


    print(clock.fps())

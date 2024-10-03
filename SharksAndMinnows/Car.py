from mqtt import MQTTClient
from machine import Pin
import time
import network

class Car:
    def __init__(self, motorPin):
        self.motor = Pin(motorPin, Pin.OUT)

    def drive(self):
        self.motor.on()
    
    def brake(self):
        self.motor.off()

# Handles internet connections (must change ssid and password)
def internet():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('Tufts_Robot', '')

    while wlan.ifconfig()[0] == '0.0.0.0':
        print('.', end=' ')
        time.sleep(1)

    # We should have a valid IP now via DHCP
    print(wlan.ifconfig())


# Callback function for MQTT. Sets global enable
def callback(topic, msg):
    command = msg.decode()
    print((topic.decode(), msg.decode()))
    if command == 'drive':
        porche.drive()
    if command == 'brake':
        porche.brake()

# MQTT initialization and handler function
def mqtt():
    mqtt_broker = 'broker.hivemq.com' 
    port = 1883
    topic_sub = 'ME35-24/cory'

    client = MQTTClient('ME35_cory', mqtt_broker , port, keepalive=60)
    client.connect()
    client.set_callback(callback)          # set the callback if anything is read
    client.subscribe(topic_sub.encode())   # subscribe to a bunch of topics
    
    while True:
        client.check_msg()
        print("listening")
        time.sleep(0.01)

porche = Car('GPIO1')
internet()
mqtt()
import time
from networking import Networking

#Initialise
networking = Networking()

################### SENDING MESSAGES ###################
recipient_mac = b'\xFF\xFF\xFF\xFF\xFF\xFF' #This mac sends to all
message =  'hello'
while True:
    networking.aen.send(recipient_mac, message)
    time.sleep(1)
########################################################

################## RECEIVING MESSAGES ##################
def receive():
        print("Receive")
        for mac, message, rtime in networking.aen.return_messages(): #You can directly iterate over the function
            print(mac, message, rtime)
while True:
    networking.aen.irq(receive())
    time.sleep(0.5)
########################################################

# while True:
#     lastmsg = str(networking.aen.irq(receive))
#     #convert lastmsg to just the id number
#     colon = 0
#     idnumber = ''
#     for i in lastmsg:
#         print(i)
#         if i == ":":
#             colon +=1
#         if colon == 2:
#             idnumber = idnumber + i
#     print(idnumber)
#     time.sleep(0.5)

# #Print own mac
# print(networking.sta._sta.config('mac'))
# print()

# #Ping, calculates the time until you receive a response from the peer
# networking.aen.ping(recipient_mac)
# print()

# #Echo, sends a message that will be repeated back by the recipient
# networking.aen.echo(recipient_mac, message)
# print()

#Message, sends the specified message to the recipient, supported formats are bytearrays, bytes, int, float, string, bool, list and dict, if above 241 bytes, it will send in multiple packages: max 60928 bytes
# while True:
#     networking.aen.send(recipient_mac, message)
#     print()
#     time.sleep(3)

# #Check if there are any messages in the message buffer
# print(networking.aen.check_messages())
# print()

# #Get Last Received Message
# print(networking.aen.return_message()) #Returns none, none, none if there are no messages
# print()

#Get the RSSI table
print(networking.aen.rssi())
print()

# #Get All Recieved Messages
# messages = networking.aen.return_messages()
# for mac, message, receive_time in messages:
#     print(mac, message, receive_time)


networking.aen.irq(receive) #interrupt handler
print(networking.aen._irq_function)

time.sleep(0.05)#There is a bug in thonny with some ESP32 devices, which makes this statement necessary. I don't know why, currently discussing and debugging this with thonny devs.
from networking import Networking
import time

#Initialise
networking = Networking()

###Example code###

recipient_mac = b'\x54\x32\x04\x33\x48\x14' #This mac sends to all
message =  b'T2\x04!a\x9c'

# # Get All Recieved Messages
# messages = networking.aen.return_messages()
# for mac, message, receive_time in messages:
#     print(mac, message, receive_time)
    
#Set up an interrupt which runs a function as soon as possible after receiving a new message
def receive():
    global x
    for mac, message, rtime in networking.aen.return_messages(): #You can directly iterate over the function
        msg = message
        x = mac
    return str(msg)

while True:

    msg = (networking.aen._irq(receive())) #interrupt handler
    print(x)

    # if msg == dragon':
    #     networking.aen.send(recipient_mac, message)
    #     print("I am out of the game")
    


    #print(networking.aen._irq_function)
    

   
    
    time.sleep(1)
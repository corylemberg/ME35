import time

counter = 0

while True:
    time.sleep(0.1)
    counter += 1
    seconds = counter / 10
    print(f'Seconds {seconds}' ,end='\r')
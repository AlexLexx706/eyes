import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) #Set GPIO to pin numbering
PIR = 24 #Assign pin 8 to PIR
GPIO.setup(PIR, GPIO.IN) #Setup GPIO pin PIR as input
time.sleep(2) #Give sensor time to startup

try:
    while True:
        if GPIO.input(PIR):
            print ("Motion Detected!")
        else:
            print ("no motion")
        time.sleep(0.5)

except KeyboardInterrupt: #Ctrl+c
    pass #Do nothing, continue to finally
finally:
    GPIO.cleanup() #reset all GPIO
    print ("Program ended")
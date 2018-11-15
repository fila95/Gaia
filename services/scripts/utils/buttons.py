import RPi.GPIO as GPIO
import time

global buttons 
buttons = [14]

#function to be called to initialize buttons
def setup():
    for button in buttons:
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Waits for the first pressed button and returns its index. This function is blocking.
def waitForInput():
    hasBeenPressed = False
    while (not hasBeenPressed):
        for i in range(0, len(buttons)):
            input_state = GPIO.input(buttons[i])
            if input_state == True:
                print("pressed ", i)
                return i
        time.sleep(0.3)
    return -1
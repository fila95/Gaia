import RPi.GPIO as GPIO
import sched, time
from threading import Thread
from pygame import mixer # Load the required library

global hasBeenPressed
hasBeenPressed = False

def attractChild():
    global hasBeenPressed
    while (not hasBeenPressed):
        GPIO.output(LIGHT,True)
        mixer.music.play()
        time.sleep(10)
        mixer.music.stop()
        GPIO.output(LIGHT, False)
        time.sleep(10)

def waitForInput():
    global hasBeenPressed
    while (not hasBeenPressed):
        input_state = GPIO.input(BUTTON)
        if input_state == True:
            print("pressed")
            hasBeenPressed = True
        time.sleep(0.3)

print("running")

GPIO.setmode (GPIO.BCM)
LIGHT = 4
BUTTON = 19

GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LIGHT, GPIO.OUT)

mixer.init()
#TODO change path
m = mixer.music.load('../05. AC DC - T.N.T..mp3')
mixer.music.set_volume(1.0)

t1 = Thread(target=waitForInput, args=())
t2 = Thread(target=attractChild, args=())
t1.start()
t2.start()
t1.join()
t2.join()
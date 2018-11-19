import RPi.GPIO as GPIO
import time
from utils.buttons import *
from threading import Thread
from pygame import mixer # Load the required library


global gameStarted

def waitForChild():
    global gameStarted
    if (waitForInput() != -1):
        print("gameStarted = True")
        gameStarted = True

def attractChild():
    global gameStarted
    #select track to attract children
    #TODO change path
    m = mixer.music.load('../05. AC DC - T.N.T..mp3')
    mixer.music.set_volume(1.0)
    while (not gameStarted):
        GPIO.output(LIGHT1,True)
        GPIO.output(LIGHT2,True)
        mixer.music.play()
        time.sleep(10)
        mixer.music.stop()
        GPIO.output(LIGHT1, False)
        GPIO.output(LIGHT2,True)
        time.sleep(10)

print("Running")

#PREPARE THE ENVIRONMENT
GPIO.setmode (GPIO.BCM)
LIGHT1 = 4
LIGHT2 = 3

buttons = Buttons();
GPIO.setup(LIGHT1, GPIO.OUT)
GPIO.setup(LIGHT1, GPIO.OUT)

mixer.init()

#START GAME
gameStarted = False

#create threads that continously make sounds and music and wait for a child to start the game
t1 = Thread(target=waitForChild, args=())
t2 = Thread(target=attractChild, args=())
t1.start()
t2.start()
t1.join()
t2.join()

#CHECK IF IT IS A NEW GAME
m = mixer.music.load('../05. AC DC - T.N.T..mp3')
GPIO.output(LIGHT1,True)
GPIO.output(LIGHT2,True)

i = waitForInput()

if(i == 0)
    #new game
else if(i == 1)
    #continuing already started game


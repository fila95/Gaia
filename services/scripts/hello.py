#!/usr/bin/python
 
from time import sleep
from neopixel import *
 
try:
    while True:
        print("Hello World")
        sleep(60)
except KeyboardInterrupt, e:
    logging.info("Stopping...")
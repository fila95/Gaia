from neopixel import *
from Dot import Dot
from DotColor import *

import time
import asyncio
import sys
import random

class DotManager:

	# Number of light disks
	DOTS_COUNT = 1

	# GPIO pin connected to the pixels (18 uses PWM!).
	LED_PIN = 18
	# GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
	#LED_PIN = 10
	# LED signal frequency in hertz (usually 800khz)
	LED_FREQ_HZ = 800000
	# DMA channel to use for generating signal (try 10)
	LED_DMA = 10
	# True to invert the signal (when using NPN transistor level shift)
	LED_INVERT = False
	# set to '1' for GPIOs 13, 19, 41, 45 or 53
	LED_CHANNEL = 0

	def __init__(self, callback = None):
		self.callback = callback
		self.led_count = self.DOTS_COUNT * Dot.LED_COUNT
		self.dot_pins = [23, 24, 25, 8, 7, 1]

		# Create NeoPixel object with appropriate configuration.	
		self.strip = Adafruit_NeoPixel(self.led_count, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, 255, self.LED_CHANNEL)

    	# Intialize the library (must be called once before other functions).
		self.strip.begin()
		
		# Configure all dots
		self.dots = []
		self._configure()
		
			

	def setColor(self, color):
		for i in range(0, self.DOTS_COUNT):
			self.dots[i].setColor(color)

	def tapped(self, index: int, dot: Dot):
		if self.callback is not None:
			self.callback(index, dot)

	def _configure(self):
		for i in range(0, self.DOTS_COUNT):
			start_index = i*int(Dot.LED_COUNT)
			dot = Dot(strip=self.strip, led_start_index=start_index, button_pin=self.dot_pins[i], cb=self.tapped)
			self.dots.append(dot)
		
			





loop = None

def callback(index, dot):
	print(index)
	dot.setColor(Colors.random())

if __name__ == '__main__':
	try:
		manager = DotManager(callback=callback)
		manager.setColor(Colors.random())
		

        # run the event loop
		loop = asyncio.get_event_loop()
		loop.run_forever()
		loop.close()
	except:
		print("Error:", sys.exc_info()[0])

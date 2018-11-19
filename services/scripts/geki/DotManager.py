from neopixel import *
from Dot import Dot
from DotColor import *

import time
import asyncio
import sys
import random
import logging

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

	def __init__(self, tapHandler = None):
		self.tapHandler = tapHandler
		self.led_count = self.DOTS_COUNT * Dot.LED_COUNT
		self.dot_pins = [23, 24, 25, 8, 7, 1]

		# Create NeoPixel object with appropriate configuration.	
		self.__strip = Adafruit_NeoPixel(self.led_count, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, 255, self.LED_CHANNEL)

    	# Intialize the library (must be called once before other functions).
		self.__strip.begin()
		
		# Configure all dots
		self.__dots = []
		self._configure()
	
	def _configure(self):
		for i in range(0, self.DOTS_COUNT):
			start_index = i*int(Dot.LED_COUNT)
			dot = Dot(strip=self.__strip, led_start_index=start_index, button_pin=self.dot_pins[i], cb=self.tapped)
			self.__dots.append(dot)
		logging.info("DotManager initialized successfully")

	
	def getDots(self):
		return self.__dots

	def setColor(self, color):
		for i in range(0, self.DOTS_COUNT):
			self.__dots[i].setColor(color)
	
	def setBrightness(self, brightness: int):
		for i in range(0, self.DOTS_COUNT):
			self.__dots[i].setBrightness(brightness)

	def tapped(self, index: int, dot: Dot):
		logging.info("Dot at index:{:d} was tapped.".format(index))
		if self.tapHandler is not None:
			self.tapHandler(index, dot)

	def setColors(self, colors):
		if len(colors) == self.DOTS_COUNT:
			for i in range(0, self.DOTS_COUNT):
				self.__dots[i].setColor(colors[i])
		else:
			logging.error("colors should be same length as dots")

		pass
	
		
	





loop = None

def dotWasTapped(index, dot):
	print("Tapped Dot at index: ", end="", flush=True)
	print(index)
	# dot.setBrightness(random.randrange(0, 255, 1))
	dot.setColor(Colors.random())

if __name__ == '__main__':
	try:
		manager = DotManager(tapHandler=dotWasTapped)
		manager.setColor(Colors.random())
		manager.setBrightness(80)

        # run the event loop
		loop = asyncio.get_event_loop()
		loop.run_forever()
		loop.close()

	except:
		print("Error:", sys.exc_info()[0])

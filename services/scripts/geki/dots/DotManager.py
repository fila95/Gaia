try:
	from neopixel import *
except ImportError as e:
	from neopixel_mock import Adafruit_NeoPixel, Color

from Dot import Dot
from DotColor import *

import sys
import random
import logging
import threading
import time
from queue import Queue, Empty
import asyncio

class DotManager:

	# Number of light disks
	_DOTS_COUNT = 1

	# GPIO pin connected to the pixels (18 uses PWM!).
	_LED_PIN = 18
	# GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
	#_LED_PIN = 10
	# LED signal frequency in hertz (usually 800khz)
	_LED_FREQ_HZ = 800000
	# DMA channel to use for generating signal (try 10)
	_LED_DMA = 10
	# True to invert the signal (when using NPN transistor level shift)
	_LED_INVERT = False
	# set to '1' for GPIOs 13, 19, 41, 45 or 53
	_LED_CHANNEL = 0

	def __init__(self, tapHandler = None):
		self.tapHandler = tapHandler
		self.led_count = self._DOTS_COUNT * Dot.LED_COUNT
		self.dot_pins = [23, 24, 25, 8, 7, 1]

		# Create NeoPixel object with appropriate configuration.	
		self.__strip = Adafruit_NeoPixel(self.led_count, self._LED_PIN, self._LED_FREQ_HZ, self._LED_DMA, self._LED_INVERT, 255, self._LED_CHANNEL)

    	# Intialize the library (must be called once before other functions).
		self.__strip.begin()
		
		# Configure all dots
		self.__dots = []
		self._configure()
	
	def _configure(self):
		for i in range(0, self._DOTS_COUNT):
			start_index = i*int(Dot.LED_COUNT)
			dot = Dot(strip=self.__strip, led_start_index=start_index, button_pin=self.dot_pins[i], cb=self.tapped)
			self.__dots.append(dot)
		logging.info("DotManager initialized successfully")

	
	def getDots(self):
		return self.__dots

	def setColor(self, color, fade=True):
		for i in range(0, self._DOTS_COUNT):
			self.__dots[i].setColor(color, fade=fade)

	def setColorAtIndex(self, idx: int, color, fade=True):
		if idx<self._DOTS_COUNT and idx>0:
			self.__dots[idx].setColor(color, fade=fade)
	
	def setBrightnessAtIndex(self, idx: int, brightness, fade=True):
		if idx<self._DOTS_COUNT and idx>0:
			self.__dots[idx].setBrightness(brightness, fade=fade)
	
	def setBrightness(self, brightness: int, fade=True):
		for i in range(0, self._DOTS_COUNT):
			self.__dots[i].setBrightness(brightness, fade=fade)

	def tapped(self, index: int, dot: Dot):
		logging.info("Dot at index:{:d} was tapped.".format(index))
		if self.tapHandler is not None:
			self.tapHandler(index, dot)

	def setColors(self, colors, fade=True):
		if len(colors) == self._DOTS_COUNT:
			for i in range(0, self._DOTS_COUNT):
				self.__dots[i].setColor(colors[i], fade=fade)
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
		manager.setColor(Colors.random(), fade=False)
		manager.setBrightness(255, fade=False)

        # run the event loop
		loop = asyncio.get_event_loop()
		loop.run_forever()
		loop.close()

	except:
		print("Error:", sys.exc_info()[0])

try:
	from neopixel import *
except ImportError as e:
	from .neopixel_mock import Adafruit_NeoPixel, Color

from .Dot import Dot
from .DotColor import DotColor
from .DotColor import Colors
from .DotWorker import DotWorker
from .DotAnimation import DotAnimation

import sys
import random
import logging
import time
import threading
from queue import Queue, Empty
import asyncio

class DotManager:

	# GPIO pin connected to the pixels (18 uses PWM!).
	_LED_PIN = 10
	# _LED_PIN = 18
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
		self.__tapHandler = tapHandler
		self.__dots_count = 4
		self.__led_count = self.__dots_count * Dot.LED_COUNT
		self.__dot_pins = [14, 15, 23, 24]
		

		# Create NeoPixel object with appropriate configuration.	
		self.__strip = Adafruit_NeoPixel(self.__led_count, self._LED_PIN, self._LED_FREQ_HZ, self._LED_DMA, self._LED_INVERT, 255, self._LED_CHANNEL)

		# Intialize the library (must be called once before other functions).
		self.__strip.begin()

		# Configure Animations Part
		self.animations = {
			DotAnimation.RAINBOW: self.__rainbow, 
			DotAnimation.RAINBOW_CYCLE: self.__rainbowCycle, 
			DotAnimation.THEATER_CHASE_RAINBOW: self.__theaterChaseRainbow
		}

		self.__animationAffectsLeds = False
		self.__animating = False

		self.__queue = Queue()
		self.__interrupt_event = threading.Event()
		self.__stop_event = threading.Event()
		self.__worker = DotWorker(logging, self.__strip, self.__queue, self.__stop_event, self.__interrupt_event)
		self.__worker.start()
		
		# Configure all dots
		self.__dots = []
		self.__configure()
	
	def __configure(self):
		for i in range(0, self.__dots_count):
			start_index = i*int(Dot.LED_COUNT)
			dot = Dot(strip=self.__strip, led_start_index=start_index, button_pin=self.__dot_pins[i], cb=self.__tapped, stopAnimationTrigger=self.stopAnimation)
			self.__dots.append(dot)
		logging.info("DotManager initialized successfully")

	
	def getDots(self):
		return self.__dots
	def getDotsCount(self):
		return self.__dots_count

	def setColor(self, color, fade=True):
		self.__stopAnimationIfNeeded()
		for i in range(0, self.__dots_count):
			self.__dots[i].setColor(color, fade=fade)

	def setColorAtIndex(self, idx: int, color, fade=True):
		self.__stopAnimationIfNeeded()
		if idx<self.__dots_count and idx>=0:
			self.__dots[idx].setColor(color, fade=fade)
	
	def setBrightnessAtIndex(self, idx: int, brightness, fade=True):
		self.__stopAnimationIfNeeded()
		if idx<self.__dots_count and idx>=0:
			self.__dots[idx].setBrightness(brightness, fade=fade)
	
	def setBrightness(self, brightness: int, fade=True):
		self.__stopAnimationIfNeeded()
		for i in range(0, self.__dots_count):
			self.__dots[i].setBrightness(brightness, fade=fade)

	def setColors(self, colors, fade=True):
		self.__stopAnimationIfNeeded()

		clrs = colors
		diff = len(clrs) - self.__dots_count
		if diff < 0:
			for i in range(0, abs(diff)):
				clrs.append(Colors.OFF)

		for i in range(0, self.__dots_count):
			self.__dots[i].setColor(clrs[i], fade=fade)

	def turnAllOff(self):
		self.__stopAnimationIfNeeded()
		for i in range(self.__led_count):
			self.__strip.setPixelColorRGB(i,0,0,0)
		self.__strip.show()
	
	def animate(self, animation=DotAnimation.RAINBOW, keep_running=False):
		self.__stopAnimationIfNeeded()
		self.__animating = True
		self.__run_animation(animation=animation, kwargs={"keep_running": keep_running})
	
	def stopAnimation(self):
		self.__stopAnimationIfNeeded()

	def __tapped(self, index: int, dot: Dot):
		logging.info("Dot at index:{:d} was tapped.".format(index))
		if self.__tapHandler is not None:
			self.__tapHandler(index, dot)

	def setAnimationAffectDots(self, affectsDots=True):
		self.__animationAffectsLeds = not affectsDots
	
	def setAnimationAffectLeds(self, affectsLeds=True):
		self.__animationAffectsLeds = affectsLeds

	
	
	## Color Animation Part
	def __stopAnimationIfNeeded(self):
		if self.__animating:
			self.__animating = False
			self.__clearQueue(interrupt=True)

	def __handle_async(self, lfunc, interrupt=True):
		# ql = self.__queue.qsize()
		if(interrupt == True and not self.__queue.empty() and not self.__interrupt_event.isSet()):
			self.__interrupt_event.set()
		self.__queue.put(lfunc)

	def __run_animation(self, animation=DotAnimation.RAINBOW, interrupt=False, kwargs=None):
		if not isinstance(animation, DotAnimation):
			return
		if not animation in self.animations:
			raise ValueError("Unknown animation " +animation)
		func = self.animations[animation]
		if kwargs is not None and "color" in kwargs:
			c = kwargs["color"]
			kwargs["color"] = Color(c[0], c[1], c[2])
		# else:
			# kwargs["color"] = Color(100, 100, 100)

		# logging.info("Running " + func.__name__ + " with args " + str(kwargs))
		lfunc = (lambda: func()) if kwargs is None else (lambda: func(**kwargs))
		self.__handle_async(lfunc, interrupt)



	# Define functions which animate LEDs in various ways.
	# ** ASYNC **
	
	def __wheel(self, pos):
		"""Generate rainbow colors across 0-255 positions."""
		if pos < 85:
			return Color(pos * 3, 255 - pos * 3, 0)
		elif pos < 170:
			pos -= 85
			return Color(255 - pos * 3, 0, pos * 3)
		else:
			pos -= 170
			return Color(0, pos * 3, 255 - pos * 3)

	def __dot_wheel(self, pos):
		"""Generate rainbow colors across 0-255 positions."""
		if pos < 85:
			return DotColor(red=pos*3, green=255-pos*3, blue=0)
		elif pos < 170:
			pos -= 85
			return DotColor(red=255-pos*3, green=0, blue=pos*3)
		else:
			pos -= 170
			return DotColor(red=0, green=pos*3, blue=255-pos*3)

	def __rainbow(self, keep_running=False, wait_ms=20, iterations=1):
		"""Draw rainbow that fades across all pixels at once."""
		for j in range(256*iterations):
			if self.__interrupt_event.isSet():
				break
			if self.__animationAffectsLeds:
				for i in range(self.__strip.numPixels()):
					self.__strip.setPixelColor(i, self.__wheel((i+j) & 255))
				self.__strip.show()
			else:
				for i in range(self.__dots_count):
					self.__dots[i].setColor(self.__dot_wheel((i+j) & 255), fade=False, stopGlobalAnimation=False)
			
			time.sleep(wait_ms/1000.0)

		if keep_running and not self.__interrupt_event.isSet():
			self.__rainbow(keep_running=keep_running, wait_ms=wait_ms, iterations=iterations)

	def __rainbowCycle(self, keep_running=False, wait_ms=20, iterations=5):
		"""Draw rainbow that uniformly distributes itself across all pixels."""
		for j in range(256*iterations):
			if self.__interrupt_event.isSet():
				break
			
			if self.__animationAffectsLeds:
				for i in range(self.__strip.numPixels()):
					self.__strip.setPixelColor(i, self.__wheel((int(i * 256 / self.__strip.numPixels()) + j) & 255))
				self.__strip.show()
			else:
				for i in range(self.__dots_count):
					self.__dots[i].setColor(self.__dot_wheel((int(i * 256 / self.__dots_count) + j) & 255), fade=False, stopGlobalAnimation=False)
			
			time.sleep(wait_ms/1000.0)
		
		if keep_running and not self.__interrupt_event.isSet():
			self.__rainbowCycle(keep_running=keep_running, wait_ms=wait_ms, iterations=iterations)

	def __theaterChaseRainbow(self, keep_running=False, wait_ms=50):
		"""Rainbow movie theater light style chaser animation."""
		for j in range(256):
			if self.__interrupt_event.isSet():
				break
			for q in range(3):

				if self.__animationAffectsLeds:
					for i in range(self.__strip.numPixels()):
						self.__strip.setPixelColor(i+q, self.__wheel((i+j) % 255))
					self.__strip.show()
				else:
					for i in range(self.__dots_count):
						if i+q < self.__dots_count:
							self.__dots[i+q].setColor(self.__dot_wheel((i+j) % 255), fade=False, stopGlobalAnimation=False)
						
				time.sleep(wait_ms/1000.0)
				if self.__animationAffectsLeds:
					for i in range(self.__strip.numPixels()):
						self.__strip.setPixelColor(i+q, 0)
					self.__strip.show()
				else:
					for i in range(self.__dots_count):
						if i+q < self.__dots_count:
							self.__dots[i+q].setColor(DotColor(0, 0, 0), fade=False, stopGlobalAnimation=False)

		if keep_running and not self.__interrupt_event.isSet():
			self.__theaterChaseRainbow(keep_running=keep_running, wait_ms=wait_ms)

	def __close(self):
		#interrupt running task
		self.__interrupt_event.set()
		#stop loop and end-thread
		self.__stop_event.set()
		self.__strip.__del__()

	def __clearQueue(self, interrupt=False):
		#consume items first
		while not self.__queue.empty():
			self.__queue.get()
		#then interrupt thead
		if(interrupt == True):
			self.__interrupt_event.set()
	

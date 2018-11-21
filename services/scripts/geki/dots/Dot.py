from DotColor import DotColor, Colors
from DotWorker import DotWorker

import pigpio
import logging
import threading
import time
from queue import Queue, Empty
try:
	from neopixel import *
except ImportError as e:
	from neopixel_mock import Adafruit_NeoPixel, Color

class Dot:
	LED_COUNT = 4

	def __init__(self, strip, led_start_index, button_pin, cb, stopAnimationTrigger):
		self.strip = strip
		self.cb = cb
		self.stopAnimationTrigger = stopAnimationTrigger
		self.led_start_index = int(led_start_index)
		self.button_pin = int(button_pin)
		self.__targetColor = DotColor(255, 255, 255)
		self.__currentColor = self.__targetColor
		self.__targetBrightnessedColor = self.__targetColor
		self.__brightness = 255

		self.queue = Queue()
		self.interrupt_event = threading.Event()
		self.stop_event = threading.Event()

		self._worker = DotWorker(logging, self.strip, self.queue, self.stop_event, self.interrupt_event)
		self._worker.start()

		cb = pigpio.pi()
		cb.callback(self.button_pin, edge=0, func=self.__callback)
		# self.showColor(self.__targetColor)


	def __handle_async(self, lfunc, interrupt=True):
		# ql = self.queue.qsize()
		if(interrupt == True and not self.queue.empty() and not self.interrupt_event.isSet()):
			self.interrupt_event.set()
		self.queue.put(lfunc)

	def __run_fade_animation(self):
		lfunc = self._fade
		self.__handle_async(lfunc, True)

	def setColor(self, color: DotColor, fade=True):
		self.stopAnimationTrigger()
		if fade:
			self.clearQueue(interrupt=False)
		
		logging.info("Setting color of dot:{:d} to r: {:d}, g: {:d}, b: {:d}.".format(self.led_start_index, color.red, color.green, color.blue))
		self.__targetColor = color
		self.showColor(color, fade=fade)


	def setBrightness(self, brightness: int, fade=True):
		self.stopAnimationTrigger()
		if fade:
			self.clearQueue(interrupt=False)
		
		logging.info("Setting brightness of dot:{:d} to {:d}.".format(self.led_start_index, brightness))
		self.__brightness = max(0, min(brightness, 255))
		if self.__targetColor is not None:
			self.setColor(self.__targetColor, fade=fade)


	def showColor(self, color: DotColor, fade=False):
		# Normalize brightness
		col = color
		if isinstance(col, Colors):
			col = color.value
		self.__targetBrightnessedColor = self.__generateBrightnessedColorFrom(col)

		if fade is False:
			self.__currentColor = self.__targetBrightnessedColor
			for i in range(self.led_start_index, self.led_start_index+self.LED_COUNT):
				self.strip.setPixelColor(i, Color(self.__currentColor.red, self.__currentColor.green, self.__currentColor.blue))
			self.strip.show()
		else:
			self.__run_fade_animation()
			pass


	def getColor(self):
		return self.__targetColor

	def getBrightnessedAppliedColor(self):
		return self.__targetBrightnessedColor

	# ** ASYNC **
	def __generateBrightnessedColorFrom(self, color):
		bright = float(self.__brightness) / 255
		red = int(float(color.red) * bright)
		green = int(float(color.green) * bright)
		blue = int(float(color.blue) * bright)
		col = DotColor(red=red, green=green, blue=blue)
		return col

	def _fade(self, wait_ms=10, iterations=10):
		"""Fade Colors."""

		for j in range(iterations):
			if self.interrupt_event.isSet():
				break

			col = self.__currentColor
			r_diff =  self.__targetBrightnessedColor.red - col.red
			g_diff = self.__targetBrightnessedColor.green - col.green
			b_diff = self.__targetBrightnessedColor.blue - col.blue

			red = col.red + int(r_diff/iterations)
			green = col.green + int(g_diff/iterations)
			blue = col.blue + int(b_diff/iterations)

			self.__currentColor = DotColor(red=red, green=green, blue=blue)
			for i in range(self.led_start_index, self.led_start_index+self.LED_COUNT):
				self.strip.setPixelColor(i, Color(self.__currentColor.red, self.__currentColor.green, self.__currentColor.blue))
			self.strip.show()

			time.sleep(wait_ms/1000.0)

	
	def close(self):
		#interrupt running task
		self.interrupt_event.set()
		#stop loop and end-thread
		self.stop_event.set()
		# self.strip.__del__()

	def clearQueue(self, interrupt=False):
		#consume items first
		while not self.queue.empty():
			self.queue.get()
		#then interrupt thead
		if(interrupt == True):
			self.interrupt_event.set()

	def __callback(self, gpio, newLevel, tick):
		self.cb(int(self.led_start_index/self.LED_COUNT), self)


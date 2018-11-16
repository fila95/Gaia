import pigpio
from neopixel import *

from DotColor import *

class Dot:
	LED_COUNT = 4

	def __init__(self, strip, led_start_index, button_pin, cb):
		self.strip = strip
		self.cb = cb
		self.led_start_index = int(led_start_index)
		self.button_pin = int(button_pin)
		self.originalColor = DotColor(255, 255, 255)
		self.brightnessedColor = self.originalColor
		self.brightness = 255

		cb = pigpio.pi()
		cb.callback(self.button_pin, edge=0, func=self.callback)

	def setColor(self, color: DotColor):
		self.originalColor = color
		self.showColor(color)


	def setBrightness(self, brightness: int):
		self.brightness = brightness
		if self.originalColor is not None:
			self.setColor(self.originalColor)


	def showColor(self, color: DotColor):
		# Normalize brightness
		col = color
		if isinstance(col, Colors):
			col = color.value

		bright = float(self.brightness) / 255

		red = int(float(col.red) * bright)
		green = int(float(col.green) * bright)
		blue = int(float(col.blue) * bright)
		self.brightnessedColor = DotColor(red=red, green=green, blue=blue)

		for i in range(self.led_start_index, self.led_start_index+self.LED_COUNT):
			self.strip.setPixelColor(i, Color(self.brightnessedColor.red, self.brightnessedColor.green, self.brightnessedColor.blue))
		self.strip.show()

	def callback(self, gpio, newLevel, tick):
		self.cb(int(self.led_start_index/self.LED_COUNT), self)

	
		
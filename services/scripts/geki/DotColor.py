from enum import Enum
import random

class DotColor:
	def __init__(self, red: int, green: int, blue: int):
		self.red = red
		self.green = green
		self.blue = blue

class Colors(Enum):
	WHITE = DotColor(red=255, green=255, blue=255)
	RED = DotColor(red=255, green=0, blue=0)
	GREEN = DotColor(red=0, green=255, blue=0)
	BLUE = DotColor(red=0, green=0, blue=255)
	OFF = DotColor(red=0, green=0, blue=0)

	@staticmethod
	def random():
		return DotColor(red=random.randrange(0, 255, 1), green=random.randrange(0, 255, 1), blue=random.randrange(0, 255, 1))
		# return random.choice(list(Colors))



	
	
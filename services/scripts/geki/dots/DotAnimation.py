from enum import Enum
import random

class DotAnimation(Enum):
	RAINBOW="rainbow"
	RAINBOW_CYCLE="rainbowCycle"
	# THEATER_CHASE="theaterChase"
	THEATER_CHASE_RAINBOW="theaterCaseRainbow"

	@staticmethod
	def random():
		return random.choice(list(DotAnimation))


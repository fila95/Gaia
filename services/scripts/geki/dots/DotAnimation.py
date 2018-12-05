from enum import Enum
import random

class DotAnimation(Enum):
	RAINBOW="RAINBOW"
	RAINBOW_CYCLE="RAINBOW_CYCLE"
	THEATER_CHASE_RAINBOW="THEATER_CHASE_RAINBOW"

	@staticmethod
	def random():
		return random.choice(list(DotAnimation))

	@staticmethod
	def fromString(str):
		if str == "RAINBOW":
			return DotAnimation.RAINBOW
		elif str == "RAINBOW_CYCLE":
			return DotAnimation.RAINBOW_CYCLE
		else:
			return DotAnimation.THEATER_CHASE_RAINBOW
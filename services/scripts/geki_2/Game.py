import logging
import threading

from GameStates import GameStates
from StoriesManager import StoryManager
from dots import *
from sound.SpeakerManager import SpeakerManager

class Game():

	def __init__(self):
		logging.info("Initializing Geki Game...")
		self.leds = DotManager(tapHandler=self.__dotWasTapped)
		logging.info("DotManager Loaded!")

		self.speakers = SpeakerManager()
		logging.info("SpeakerManager Loaded!")

		self.stories = StoryManager()
		logging.info("StoryManager Loaded!")

		## Used to ignore touches
		self.userInteractionEnabled = True
		self.touchedColors = []

		## Timer Management
		self.timer = None
		logging.info("Done!")
		

	def start(self):
		self.touchedColors = []
		self.userInteractionEnabled = True
		self.state = GameStates.IDLE
		self.leds.animate(animation=DotAnimation.RAINBOW_CYCLE, keep_running=True)


	def stop(self):
		logging.info("Stopping Geki Game...")
		self.leds.turnAllOff()
		self.speakers.deinit()


	## Private
	def __triggerWaitingFirstContactSubroutine(self):
		## Wait the first real contact, start timeout timer
		self.state = GameStates.WAITING_FIRST_CONTACT
		self.__resetTimer(duration=self.state.waitTime())
		
	def __triggerWaitingRestOfSequenceSubroutine(self):
		self.state = GameStates.WAITING_SEQUENCE
		self.__resetTimer(duration=self.state.waitTime())

		if len(self.touchedColors) == len(self.stories.availableColors()):
			self.__checkColorSequence
		
	def __checkColorSequence(self):
		self.__stopTimer()

		story = self.stories.storyForColors()
		## TODO: Check Sequence, if wrong send wrong story voice, then restart game
		pass

	def __processNextInteractionBasedOnColor(self, color):
		if self.state == GameStates.IDLE:
			self.__triggerWaitingFirstContactSubroutine()
		if self.state == GameStates.WAITING_FIRST_CONTACT:
			self.__triggerWaitingRestOfSequenceSubroutine()

		elif self.state == GameStates.WAITING_SEQUENCE:
			self.touchedColors.append(color)

		elif self.state == GameStates.TELLING_STORY:
			## Should never come here, callback from audio should manage it
			pass
		elif self.start == GameStates.ENDING:
			## Should never come here, callback from audio should manage it
			pass
			
	
	def __processNextInteractionBasedOnTimerFired(self):
		logging.info("Timer was Fired..")

		if self.state == GameStates.WAITING_FIRST_CONTACT:
			self.start()
		elif self.state == GameStates.WAITING_SEQUENCE:
			self.__checkColorSequence()
			

	def __dotWasTapped(self, index, dot):
		if not self.userInteractionEnabled:
			logging.info("Ignoring Touch..")
			return
		color = dot.getColor()
		logging.info("Tapped Dot at index: {} and color: r={}, g={}, b={}".format(index, color.red, color.green, color.blue))
		self.__processNextInteractionBasedOnColor(color)
		pass
	
	# Timers:
	def __setupTimer(self, duration=10):
		if self.timer is None:
			self.timer = threading.Timer(int(duration), self.__timerFired)
			self.timer.start()

	def __stopTimer(self):
		if self.timer is not None:
			self.timer.cancel()
			self.timer = None

	def __resetTimer(self, duration=10):
		self.__stopTimer()
		self.__setupTimer(duration=duration)

	def __timerFired(self):
		self.__processNextInteractionBasedOnTimerFired()
		pass
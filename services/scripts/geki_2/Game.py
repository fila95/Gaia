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

		self.speakers = SpeakerManager(finishPlayingCallback=self.__musicDidFinishPlaying)
		logging.info("SpeakerManager Loaded!")

		self.stories = StoryManager()
		self.current_story = None
		logging.info("StoryManager Loaded!")

		## Used to ignore touches (still not implemented)
		self.userInteractionEnabled = True
		self.touchedColors = []

		## Timer Management
		self.timer = None
		logging.info("Done!")
		

	def start(self):
		self.current_story = None
		self.touchedColors = []
		self.userInteractionEnabled = True
		self.state = GameStates.IDLE
		self.leds.setAnimationAffectDots()
		self.leds.animate(animation=DotAnimation.RAINBOW_CYCLE, keep_running=True)


	def stop(self):
		logging.info("Stopping Geki Game...")
		self.leds.turnAllOff()
		self.speakers.deinit()

	## Private
	def __triggerWaitingFirstContactSubroutine(self):
		## Wait the first real contact, start timeout timer
		self.state = GameStates.WAITING_FIRST_CONTACT
		self.leds.setColors(self.stories.availableColors(), fade=True)
		self.__resetTimer(duration=self.state.waitTime())
		
	def __triggerWaitingRestOfSequenceSubroutine(self):
		self.state = GameStates.WAITING_SEQUENCE
		self.__resetTimer(duration=self.state.waitTime())

		if len(self.touchedColors) == len(self.stories.availableColors()):
			self.__checkColorSequence

	def startTellingStory(self):
		if self.current_story is None:
			return
		self.state = GameStates.TELLING_STORY
		self.speakers.playAudio(path=self.current_story.chapterPath(colorSequence=self.touchedColors))

		self.leds.setAnimationAffectLeds()
		self.leds.animate(animation=DotAnimation.RAINBOW_CYCLE, keep_running=True)
		# After this we'll wait the speakermanager callback

	def __endGame(self):
		self.state = GameStates.ENDING
		# check if this was the last chapter
		##	if yes then audio send hooray and start again
		##	if not then show the next sequence then restart
		if self.current_story.isLastChapter(self.touchedColors):
			self.speakers.playAudio(path=self.stories.gameCompletedPath())
			self.start()
		else:
			nextSequence = self.current_story.nextSequence(self.touchedColors)
			self.leds.setColors(nextSequence, fade=True)

		self.__resetTimer(duration=self.state.waitTime())
		
	def __checkColorSequence(self):
		self.__stopTimer()

		self.current_story = self.stories.storyForColors(self.touchedColors)
		if self.current_story is None:
			self.speakers.playAudio(self.stories.wrongChoicePath())
			self.start()
		else:
			self.startTellingStory()
		
	
	## Interaction Processing
	def __processNextInteractionBasedOnColor(self, color):
		# Tapped Dot
		if self.state == GameStates.IDLE:
			self.__triggerWaitingFirstContactSubroutine()
		elif self.state == GameStates.WAITING_FIRST_CONTACT:
			self.__triggerWaitingRestOfSequenceSubroutine()
		elif self.state == GameStates.WAITING_SEQUENCE:
			self.touchedColors.append(color)
			
	
	def __processNextInteractionBasedOnTimerFired(self):
		# Timer Fired
		if self.state == GameStates.WAITING_FIRST_CONTACT:
			self.start()
		elif self.state == GameStates.WAITING_SEQUENCE:
			self.__checkColorSequence()
		elif self.state == GameStates.ENDING:
			self.start()

	def __processNextInteractionBasedOnMusicFinishedPlaying(self):
		# Music finished
		if self.state == GameStates.TELLING_STORY:
			self.__endGame()
				

	# Dots:
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

	# Music Playback:
	def __musicDidFinishPlaying(self):
		self.__processNextInteractionBasedOnMusicFinishedPlaying()
		pass
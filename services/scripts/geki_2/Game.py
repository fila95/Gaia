import logging
import threading

from GameStates import GameStates
from StoriesManager import StoryManager
from dots import *
from sound.SpeakerManager import SpeakerManager

class Game():

	def __init__(self):
		print("Initializing Geki Game...")
		self.leds = DotManager(tapHandler=self.__dotWasTapped)
		print("DotManager Loaded!")

		self.speakers = SpeakerManager(finishPlayingCallback=self.__musicDidFinishPlaying)
		print("SpeakerManager Loaded!")

		self.stories = StoryManager()
		self.current_story = None
		print("StoryManager Loaded!")

		## Used to ignore touches (still not implemented)
		self.userInteractionEnabled = True
		self.touchedColors = []

		## Timer Management
		self.timer = None
		print("Done!")
		

	def start(self):
		self.current_story = None
		self.touchedColors = []
		self.userInteractionEnabled = True
		self.state = GameStates.IDLE
		self.leds.setAnimationAffectDots()
		self.leds.animate(animation=DotAnimation.RAINBOW_CYCLE, keep_running=True)


	def stop(self):
		print("Stopping Geki Game...")
		self.leds.turnAllOff()
		self.speakers.deinit()

	## Private
	def __triggerWaitingFirstContactSubroutine(self):
		print("WaitingFirstContact")
		## Wait the first real contact, start timeout timer
		self.state = GameStates.WAITING_FIRST_CONTACT
		self.leds.setColors(self.stories.availableColors(), fade=True)
		self.__resetTimer(duration=self.state.waitTime())
		
	def __triggerWaitingRestOfSequenceSubroutine(self):
		print("WaitingRestOfSequence")
		self.state = GameStates.WAITING_SEQUENCE
		self.__resetTimer(duration=self.state.waitTime())

		if len(self.touchedColors) == len(self.stories.availableColors()):
			self.__checkColorSequence

	def startTellingStory(self):
		print("startTellingStory")
		if self.current_story is None:
			return
		self.state = GameStates.TELLING_STORY
		self.speakers.playAudio(path=self.current_story.chapterPath(colorSequence=self.touchedColors))

		self.leds.setAnimationAffectLeds()
		self.leds.animate(animation=DotAnimation.RAINBOW_CYCLE, keep_running=True)
		# After this we'll wait the speakermanager callback

	def __endGame(self):
		print("endGame")
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
		print("Dot Tapped")
		# Tapped Dot
		if self.state == GameStates.IDLE:
			self.__triggerWaitingFirstContactSubroutine()
		elif self.state == GameStates.WAITING_FIRST_CONTACT:
			self.__triggerWaitingRestOfSequenceSubroutine()
		elif self.state == GameStates.WAITING_SEQUENCE:
			self.touchedColors.append(color)
			
	
	def __processNextInteractionBasedOnTimerFired(self):
		print("Timer fired")
		# Timer Fired
		if self.state == GameStates.WAITING_FIRST_CONTACT:
			self.start()
		elif self.state == GameStates.WAITING_SEQUENCE:
			self.__checkColorSequence()
		elif self.state == GameStates.ENDING:
			self.start()

	def __processNextInteractionBasedOnMusicFinishedPlaying(self):
		print("Music finished Playing")
		# Music finished
		if self.state == GameStates.TELLING_STORY:
			self.__endGame()
				

	# Dots:
	def __dotWasTapped(self, index, dot):
		if not self.userInteractionEnabled:
			print("Ignoring Touch..")
			return
		color = dot.getColor()
		print("Tapped Dot at index: {} and color: r={}, g={}, b={}".format(index, color.red, color.green, color.blue))
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
		self.timer.cancel()
		self.__processNextInteractionBasedOnTimerFired()
		pass

	# Music Playback:
	def __musicDidFinishPlaying(self):
		self.__processNextInteractionBasedOnMusicFinishedPlaying()
		pass
import logging
import threading

from dots import *
from sound.SpeakerManager import SpeakerManager
from actions.Action import Action
from actions.ActionParser import ActionParser

class Game():

	def __init__(self):
		print("Initializing Geki Game...")
		self.leds = DotManager(tapHandler=self.__dotWasTapped)
		print("DotManager Loaded!")

		self.speakers = SpeakerManager(finishPlayingCallback=self.__musicDidFinishPlaying)
		print("SpeakerManager Loaded!")

		## Timer Management
		self.timer = None
		print("Done!")

		self.currentAction: Action = None
		self.currentActionIndex = 0
		self.availableActions = Action.actionParser().parse()
		

	def start(self):
		self.currentActionIndex = -1
		self.nextAction()



	def stop(self):
		print("Stopping Geki Game...")
		self.leds.turnAllOff()
		self.speakers.deinit()

	def restart(self):
		self.start()

	# Actions:
	def nextAction(self, optionalParams=None):
		self.currentActionIndex += 1
		self.__deactivateCurrentAction()
		self.currentAction = self.availableActions[self.currentActionIndex]
		self.__activateCurrentAction(optionalParams=optionalParams)

	def jumpToAction(self, id, optionalParams=None):
		act = None
		for a in self.availableActions:
			if a.identifier == id:
				act = a
				break

		if act is not None:
			self.__deactivateCurrentAction()
			self.currentAction = self.availableActions[self.currentActionIndex]
			self.__activateCurrentAction(optionalParams=optionalParams)


	def produceActions(self, actions):
		insertableIndex = self.currentActionIndex+1
		for a in actions:
			self.availableActions.insert(insertableIndex, a)
			insertableIndex+=1

	def __deactivateCurrentAction(self):
		if self.currentAction is not None:
			self.currentAction._deactivate()

	def __activateCurrentAction(self, optionalParams=None):
		if self.currentAction is not None:
			self.currentAction._activate(optionalParams=optionalParams)

	# Dots:
	def __dotWasTapped(self, index, dot):
		color = dot.getColor()
		print("Tapped Dot at index: {} and color: r={}, g={}, b={}".format(index, color.red, color.green, color.blue))
		if self.currentAction is not None:
			self.currentAction.dotWasTapped(index, dot)
		pass
	
	# Timers:
	def _setupTimer(self, duration=10):
		if self.timer is None:
			self.timer = threading.Timer(int(duration), self.__timerFired)
			self.timer.start()

	def _stopTimer(self):
		if self.timer is not None:
			self.timer.cancel()
			self.timer = None

	def _resetTimer(self, duration=10):
		self._stopTimer()
		self._setupTimer(duration=duration)

	def __timerFired(self):
		self.timer.cancel()
		if self.currentAction is not None:
			self.currentAction.timerFired()

	# Music Playback:
	def __musicDidFinishPlaying(self):
		if self.currentAction is not None:
			self.currentAction.audioDidFinishPlaying()

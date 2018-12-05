from abc import ABC, abstractmethod
import logging
import uuid

class Action(ABC):

	def __init__(self, data):
		self.dotManager = None
		self.speakerManager = None
		self._game = None
		self.__parser = Action.actionParser()
		self.identifier = str(uuid.uuid1())

	@staticmethod
	def actionParser():
		from .ActionParser import ActionParser
		parser = ActionParser()
		return parser

	@staticmethod
	def parseIdentifier():
		return 'ABSTRACT'

	# Overridable
	@abstractmethod
	def startAction(self, optionalParams=None):
		""" Called when the action starts its lifecycle optional params can be passed with nextAction from previous action """
		pass
	
	@abstractmethod
	def audioDidFinishPlaying(self):
		""" Called when audio finished playing """
		pass

	@abstractmethod
	def dotWasTapped(self, index, dot):
		""" Called when a dot was tapped """
		pass
	
	@abstractmethod
	def timerFired(self):
		""" Called when the timer fired """
		pass

	@abstractmethod
	def deactivate(self):
		""" Called when another action will be started """
		pass

	### Not Overridable
	def _activate(self, game, optionalParams=None):
		self._game = game
		self.dotManager = game.dotManager
		self.speakerManager = game.speakerManager
		self.startAction(optionalParams=optionalParams)

	def _deactivate(self):
		self._game = None
		self.deactivate()
		self.speakerManager = None
		self.dotManager = None

	### Conveniences
	def parseActionsFromFile(self, filename):
		return self.__parser.parse(filename)
	def parseActionsFromJson(self, json):
		return self.__parser.parseFromJson(json)

	def nextAction(self, optionalParams=None):
			if self._game is not None:
				self._game.nextAction(optionalParams=optionalParams)

	def produceActions(self, actions):
		if self._game is not None:
			self._game.produceActions(actions)

	def jumpToAction(self, id, optionalParams=None):
		if self._game is not None:
			self._game.jumpToAction(id, optionalParams=optionalParams)

	def restartGame(self):
		if self._game is not None:
			self._game.restart()
	
	def scheduleTimer(self, duration=10):
		if self._game is not None:
			self._game._resetTimer(duration)
	
	def stopTimer(self, duration=10):
		if self._game is not None:
			self._game._stopTimer(duration)

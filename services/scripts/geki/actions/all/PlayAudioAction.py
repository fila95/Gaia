from ..Action import Action
import os


class PlayAudioAction(Action):

	@staticmethod
	def parseIdentifier():
		return 'PLAY_AUDIO'

	def __init__(self, data):
		super().__init__(data)
		## Parse attributes
		if "path" in data:
			from config.variables import Variables
			self.path = Variables.BASE_DIR + data["path"]

	def startAction(self, optionalParams=None):
		if optionalParams is not None:
			if "path" in  optionalParams:
				from config.variables import Variables
				self.path = Variables.BASE_DIR + optionalParams["path"]

		if self.path is not None:
			self.speakerManager.playAudio(self.path)

	def deactivate(self):
		pass

	def audioDidFinishPlaying(self):
		self.nextAction()

	def dotWasTapped(self, index, dot):
		pass

	def timerFired(self):
		pass


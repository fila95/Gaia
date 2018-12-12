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
			self.path = os.path.abspath(data["path"])

	def startAction(self, optionalParams=None):
		if optionalParams is not None:
			if "path" in  optionalParams:
				self.path = os.path.abspath(optionalParams["path"])

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


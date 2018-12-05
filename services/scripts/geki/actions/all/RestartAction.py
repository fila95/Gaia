from ..Action import Action


class RestartAction(Action):

	@staticmethod
	def parseIdentifier():
		return 'RESTART'

	def __init__(self, data):
		super().__init__(data)

	def startAction(self, optionalParams=None):
		self._game.restart()
		pass

	def deactivate(self):
		pass

	def audioDidFinishPlaying(self):
		pass

	def dotWasTapped(self, index, dot):
		pass

	def timerFired(self):
		pass
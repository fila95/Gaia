from ..Action import Action


class JumpAction(Action):

	@staticmethod
	def parseIdentifier():
		return 'JUMP'

	def __init__(self, data):
		super().__init__(data)
		## Parse attributes
		self.jumpID = data["actionIdentifier"]
		self._excludedInCombinedActions = True


	def startAction(self, optionalParams=None):
		self.jumpToAction(id=self.jumpID)

	def deactivate(self):
		pass

	def audioDidFinishPlaying(self):
		pass

	def dotWasTapped(self, index, dot):
		pass

	def timerFired(self):
		pass


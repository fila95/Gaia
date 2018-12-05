from ..Action import Action


class DelayAction(Action):

	@staticmethod
	def parseIdentifier():
		return 'DELAY'

	def __init__(self, data):
		super().__init__(data)
		## Parse attributes

		self.timeout = data["timeout"]

	def startAction(self, optionalParams=None):
		self.scheduleTimer(duration=self.timeout)

	def deactivate(self):
		pass

	def audioDidFinishPlaying(self):
		pass

	def dotWasTapped(self, index, dot):
		pass

	def timerFired(self):
		self.nextAction()
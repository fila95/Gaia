from ..Action import Action


class DelayAction(Action):

	@staticmethod
	def parseIdentifier():
		return 'DELAY'

	def __init__(self, data):
		super().__init__(data)
		## Parse attributes

		self.delay = data["delay"]

	def startAction(self, optionalParams=None):
		self.scheduleTimer(duration=self.delay)

	def deactivate(self):
		pass

	def audioDidFinishPlaying(self):
		pass

	def dotWasTapped(self, index, dot):
		pass

	def timerFired(self):
		self.nextAction()
from ..Action import Action


class WaitInputAction(Action):

	@staticmethod
	def parseIdentifier():
		return 'WAIT_INPUT'

	def __init__(self, data):
		super().__init__(data)
		## Parse attributes

		self.paths = data["paths"]
		self.availableIndexes = []
		if "available_dot_indexes" in data:
			self.availableIndexes = data["available_dot_indexes"]
		self.tappedIndexes = []


	def startAction(self, optionalParams=None):
		pass

	def deactivate(self):
		pass

	def audioDidFinishPlaying(self):
		pass

	def dotWasTapped(self, index, dot):
		if len(self.availableIndexes) is not 0:
			self.nextAction()
		else:
			if index in self.availableIndexes:
				if index not in self.tappedIndexes:
					self.tappedIndexes.append(index)

				if len(self.tappedIndexes) == len(self.availableIndexes):
					self.nextAction()

	def timerFired(self):
		pass


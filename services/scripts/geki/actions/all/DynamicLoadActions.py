from ..Action import Action


class DynamicLoadAction(Action):

	@staticmethod
	def parseIdentifier():
		return 'DYNAMIC_LOAD'

	def __init__(self, data):
		super().__init__(data)
		## Parse attributes

		self.paths = data["paths"]


	def startAction(self, optionalParams=None):
		actions = []
		for actn in self.paths:
			actions.append(self.parseActionsFromFile(filename=actn))

		self.produceActions(actions)
		self.nextAction()

	def deactivate(self):
		pass

	def audioDidFinishPlaying(self):
		pass

	def dotWasTapped(self, index, dot):
		pass

	def timerFired(self):
		pass


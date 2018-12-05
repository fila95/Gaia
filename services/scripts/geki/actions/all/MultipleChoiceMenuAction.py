from ..Action import Action


class MultipleChoiceMenuAction(Action):

	@staticmethod
	def parseIdentifier():
		return 'MULTIPLE_CHOICE_MENU'

	def __init__(self, data):
		super().__init__(data)


	def startAction(self, optionalParams=None):
		pass

	def deactivate(self):
		pass

	def audioDidFinishPlaying(self):
		pass

	def dotWasTapped(self, index, dot):
		pass

	def timerFired(self):
		pass

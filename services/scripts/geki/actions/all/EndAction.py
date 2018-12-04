from ..Action import Action


class EndAction(Action):

	@staticmethod
	def parseIdentifier():
		return 'END'

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
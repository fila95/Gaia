from ..Action import Action

class StartAction(Action):

	@staticmethod
	def parseIdentifier():
		return 'START'

	def __init__(self, data):
		super().__init__(data)


	def startAction(self, optionalParams=None):
		from dots.DotAnimation import DotAnimation
		self.dotManager.setAnimationAffectDots()
		self.dotManager.animate(animation=DotAnimation.RAINBOW_CYCLE, keep_running=True)


	def deactivate(self):
		pass
	
	def audioDidFinishPlaying(self):
		pass

	def dotWasTapped(self, index, dot):
		self.nextAction()
	
	def timerFired(self):
		pass

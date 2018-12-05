from ..Action import Action


class PlayAnimationAction(Action):

	@staticmethod
	def parseIdentifier():
		return 'PLAY_ANIMATION'

	def __init__(self, data):
		super().__init__(data)
		## Parse attributes

		animStr = data["animation"]
		from dots.DotAnimation import DotAnimation
		self.animation = DotAnimation.fromString(animStr)

		if "animation_affect_dots" in data:
			self.animation_affect_dots = data["animation_affect_dots"]
		else:
			self.animation_affect_dots = True

		self.stops_at_end = data["stops_at_end"]


	def startAction(self, optionalParams=None):
		self.dotManager.setAnimationAffectDots(self.animation_affect_dots)
		self.dotManager.animate(animation=self.animation, keep_running=True)

		if self.timeout is not None:
			self.scheduleTimer(duration=self.timeout)
		else:
			self.nextAction()

	def deactivate(self):
		if self.stops_at_end:
			self.dotManager.stopAnimation()

	def audioDidFinishPlaying(self):
		self.nextAction()

	def dotWasTapped(self, index, dot):
		pass

	def timerFired(self):
		self.nextAction()


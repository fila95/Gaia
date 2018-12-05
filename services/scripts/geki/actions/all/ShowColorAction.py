

from ..Action import Action


class ShowColorAction(Action):

	@staticmethod
	def parseIdentifier():
		return 'SHOW_COLOR'

	def __init__(self, data):
		super().__init__(data)
		## Parse attributes

		self.color = []
		self.index = []
		self.fade = []
		from dots.DotColor import DotColor
		for colors in data["colors"]:
			self.color.append(DotColor(colors["red"], colors["green"], colors["blu"]))
			self.index.append(colors["index"])
			self.fade.append(colors["fade"])


	def startAction(self, optionalParams=None):

		for ind in range(0,len(self.index)):
			dot = self.dotManager.getDots(self.index[ind])
			dot.setColor(color=self.color[ind],fade=self.fade[ind])

		if self.timeout is not None:
			self.scheduleTimer(duration=self.timeout)
		else:
			self.nextAction()

	def deactivate(self):
		pass

	def audioDidFinishPlaying(self):
		pass

	def dotWasTapped(self, index, dot):
		pass

	def timerFired(self):
		self.nextAction()
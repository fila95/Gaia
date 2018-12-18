

from ..Action import Action


class ShowColorAction(Action):

	@staticmethod
	def parseIdentifier():
		return 'SHOW_COLOR'

	def __init__(self, data):
		super().__init__(data)
		## Parse attributes

		self.colors = []
		self.indexes = []
		self.color = None

		self.fade = True


		if "fade" in data:
			self.fade = data["fade"]

		from dots.DotColor import DotColor

		if "colors" in data:
			for colors in data["colors"]:
				self.colors.append(DotColor(red=colors["color"]["red"], green=colors["color"]["green"], blue=colors["color"]["blue"]))
				# print("Show Colors: ", int(colors["color"]["red"]), int(colors["color"]["green"]), int(colors["color"]["blue"]))
				self.indexes.append(colors["index"])
		else:
			self.color = DotColor(red=data["color"]["red"], green=data["color"]["green"], blue=data["color"]["blue"])


	def startAction(self, optionalParams=None):

		if self.color is not None:
			self.dotManager.setColor(color=self.color, fade=self.fade)
		else:
			for ind in range(0, len(self.indexes)):
				self.dotManager.setColorAtIndex(idx=self.indexes[ind], color=self.colors[ind], fade=self.fade)

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
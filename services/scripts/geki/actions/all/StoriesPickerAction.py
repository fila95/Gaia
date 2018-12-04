from ..Action import Action
from ..utils.Story import Story

class StoriesPickerAction(Action):

	@staticmethod
	def parseIdentifier():
		return 'STORIES_PICKER'

	def __init__(self, data):
		super().__init__(data)
		## Parse attributes
		self.availableStories = []
		for story in data["availableStories"]:
			self.availableStories.append(Story(data=story))


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


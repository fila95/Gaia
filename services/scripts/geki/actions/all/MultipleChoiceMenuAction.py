from ..Action import Action
from enum import Enum


class ChoiceMenuState(Enum):
	START="START"
	FIRST_CHOICE_TAKEN = "FIRST_CHOICE_TAKEN"

class MultipleChoiceMenuAction(Action):

	@staticmethod
	def parseIdentifier():
		return 'MULTIPLE_CHOICE_MENU'

	def __init__(self, data):
		super().__init__(data)

		self.choiceState = ChoiceMenuState.START

		from dots.DotColor import DotColor
		self.options = []
		for opt in data["options"]:
			self.options.append(DotColor(red=opt["red"], green=opt["green"], blue=opt["blue"]))

		self.allowedSequences = data["allowed_sequences"]
		self.wrongSequenceActions = self.parseActionsFromJson(data["wrong_sequence_actions"])
		self.abortActions = self.parseActionsFromJson(data["abort_actions"])

		self.timeBetweenChoices = 1
		if "time_between_choices" in data:
			self.timeBetweenChoices = data["time_between_choices"]

		self.selectedIndexes = []


	def startAction(self, optionalParams=None):
		self.dotManager.setColors(colors=self.options, fade=True)

		if self.timeout is not None:
			self.scheduleTimer(self.timeout)


	def deactivate(self):
		pass

	def audioDidFinishPlaying(self):
		pass

	def dotWasTapped(self, index, dot):
		self.choiceState = ChoiceMenuState.FIRST_CHOICE_TAKEN
		self.selectedIndexes.append(index)
		self.scheduleTimer(self.timeBetweenChoices)

	def __evaluate(self):
		found = False
		actions = None
		for c in self.allowedSequences:
			if self.__checkItems(c["chosen_options"], self.selectedIndexes):
				found = True
				actions = self.parseActionsFromJson(c["actions"])
				break

		if found:
			self.produceActions(actions)
		else:
			self.produceActions(self.wrongSequenceActions)
		self.nextAction()


	def __checkItems(self, a, b):
		if not (len(a) == len(b)):
			return False

		same = True
		for i in range(0, len(a)-1):
			if not(a[i] == b[i]):
				same = False
				break
		return same



	def timerFired(self):
		if self.choiceState == ChoiceMenuState.START:
			self.produceActions(self.abortActions)
			self.nextAction()
		else:
			self.__evaluate()

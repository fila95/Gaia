import json

from .Action import Action
from .all import *

class ActionParser():

	def __init__(self):
		pass

	def _actions(self):
		return { cls.parseIdentifier(): cls for cls in Action.__subclasses__() }

	def parse(self, filename="config/Actions.json"):
		available = self._actions()

		with open(filename) as json_file:
			data = json.load(json_file)

		exports = []
		for actn in data:
			initializableAction = available[actn['parseIdentifier']]
			newAction = initializableAction(data=actn['attributes'])
			if "identifier" in actn:
				newAction.identifier = actn["identifier"]
			exports.append(newAction)
			
		return exports
		

	

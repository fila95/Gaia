import json

from .Action import *
from .all import *

class ActionParser():

	def __init__(self):
		pass

	def _actions(self):
		return { cls.parseIdentifier(): cls for cls in Action.__subclasses__() }

	def parse(self, filename):
		with open(filename) as json_file:
			data = json.load(json_file)
		return self.__parse(data)


	def parseFromJson(self, json):
		return self.__parse(json)

	def parseSingleAction(self, json):
		available = self._actions()
		initializableAction = available[json['parseIdentifier']]
		newAction = initializableAction(data=json['attributes'])
		if "identifier" in json:
			newAction.identifier = json["identifier"]
		if "timeout" in json:
			newAction.timeout = json["timeout"]

	def __parse(self, data):
		available = self._actions()

		exports = []
		for actn in data:
			initializableAction = available[actn['parseIdentifier']]
			newAction = initializableAction(data=actn['attributes'])
			if "identifier" in actn:
				newAction.identifier = actn["identifier"]
			if "timeout" in actn:
				newAction.timeout = actn["timeout"]
			exports.append(newAction)

		return exports


	

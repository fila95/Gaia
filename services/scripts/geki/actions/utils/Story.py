
class Story:

	def __init__(self, data):
		self.name = data["name"]
		self.definitionPath = data["definitionPath"]

		from dots.DotColor import DotColor
		self.initialColor = DotColor(
			red=data["initialColor"]["red"],
			green=data["initialColor"]["green"],
			blue=data["initialColor"]["blue"]
		)

	def actions(self, parser):
		return parser.parse(self.definitionPath)
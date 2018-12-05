from actions.Action import Action

parser = Action.actionParser()
items = parser.parse(filename="config/Actions.json")
print(items)
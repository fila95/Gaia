from actions.Action import Action

parser = Action.actionParser()
items = parser.parse()
print(items)
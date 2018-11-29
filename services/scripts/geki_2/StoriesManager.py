import json

from services.scripts.geki_2.Story import Story
from services.scripts.geki_2.dots import DotColor, Colors


class StoryManager:

    __stories = []

    def __init__(self, json1="Stories.json"):

        with open(json1) as json_file:
            data = json.load(json_file)

        for story in data['Story']:
            name = story['Name']
            colorSequence = []
            path = []

            for color in story['Colors']:
                colorSequence.append(DotColor(color['red'], color['blu'], color['green']))
            for path in story['Paths']:
                path.append(path['path'])

            self.__stories.append(Story(name, colorSequence, path))

    def returnStory(self, color=[]):
        for story in self.__stories:
            if story.initialColor().equals(color):
                return story
        return None

    def returnPossibleColor(self, index=-1):
        if index == -1:
            return None
        else:
            sequenceOfColor = []
            for story in self.__stories:
                sequenceOfColor.append(story.chaptrColor(index))
            if len(sequenceOfColor) < 6:
                sequenceOfColor = self.generateNewColor(sequenceOfColor, 6-len(sequenceOfColor))
            return sequenceOfColor

    def generateNewColor(self, sequenceOfColor, numberOfNewColor):

        count = 0

        while count < numberOfNewColor:
            newColor = Colors.random()
            check = True
            for color in sequenceOfColor:
                if color.equals(newColor):
                    check = False
            if check:
                sequenceOfColor.append(newColor)
                count = count + 1

        return sequenceOfColor


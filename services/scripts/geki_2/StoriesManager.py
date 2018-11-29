import json

from services.scripts.geki_2.Story import Story
from services.scripts.geki_2.dots import DotColor

class StoryManager:

    __stories = []
    __Colors = []

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
        for color in data['AvailableColors']:
            self.__Colors.append(DotColor(color['red'], color['blu'], color['green']))

    def returnStory(self, color=[]):
        for story in self.__stories:
            if story.initialColor().equals(color):
                return story
        return None

    def availableColors(self):
        return self.__Colors
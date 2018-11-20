
import xml.etree.ElementTree
from DotColor import Colors

class StoriesColorManager():

    colorMatrix = []

    def __init__(self, path):
        tree = xml.etree.ElementTree.parse(path)
        for story in tree.getroot():
            temporary_list = []
            for color in story.find('sequence'):
                temporary_list.append(Colors[color.text.upper()])
            self.colorMatrix.append(temporary_list)

    def getColor(self, story, part):
        return self.colorMatrix[story][part]
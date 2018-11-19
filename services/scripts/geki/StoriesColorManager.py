
import xml.etree.ElementTree
from DotColor import Colors

class StoriesColorManager():

    colorMatrix = []

    def __init__(self, path):
        tree = xml.etree.ElementTree.parse(path)
        i = 0
        for story in tree.getroot():
            self.colorMatrix.append([])
            for color in story.find('sequence'):
                self.colorMatrix[i].append(Colors[color.text.upper()])
            i+=1

    def getColor(self, story, part):
        return self.colorMatrix[story][part]
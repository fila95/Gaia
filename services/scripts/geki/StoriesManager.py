
import xml.etree.ElementTree
from geki.dots.DotColor import Colors
from geki.Chapter import Chapter


class StoriesManager():

    __chapterMatrix = []

    def __init__(self, path):
        xmlTree = xml.etree.ElementTree.parse(path)
        for story in xmlTree.getroot():
            temporary_list = []
            storyId = story.attrib["id"]
            for chapter in story:
                chapterId = chapter.attrib["id"]
                tree = chapter.find("tree").text
                color = Colors[chapter.find("color").text.upper()]
                path = chapter.find("audio").attrib["path"]
                chapter_obj = Chapter(storyId, chapterId, tree, color, path)
                temporary_list.append(chapter_obj)
            self.__chapterMatrix.append(temporary_list)

    def getColor(self, story, part):
        return self.__chapterMatrix[story][part].getColor()

    def getAudioPath(self, story, part):
        return self.__chapterMatrix[story][part].getAudioPath()

    def getTree(self, story, part):
        return self.__chapterMatrix[story][part].getTree()

    def getStoriesStartingFromTree(self, treeId):
        stories = []
        for story in self.__chapterMatrix:
            if(story[0].getTree() == treeId):
                stories.append(story[0].getStoryId())
        return stories

    def getStoryId(self, colorList):
        for story in self.__chapterMatrix:
            i = 0
            found = True
            for chapter in story:
                if not chapter.getColor.equals(colorList[i]):
                    found = False
            if found:
                return chapter.getStoryId()
        return -1

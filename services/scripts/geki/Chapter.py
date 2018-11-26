

class Chapter():
    def __init__(self, storyId, chapterId, tree:int, color, audioPath):
        self.__storyId = storyId
        self.__chapterId = chapterId
        self.__tree = tree
        self.__color = color
        self.__audioPath = audioPath
    
    def getTree(self):
        return self.__tree
    
    def getColor(self):
        return self.__color
    
    def getAudioPath(self):
        return self.__audioPath
    
    def getChapterId(self):
        return self.__chapterId
    
    def getStoryId(self):
        return self.__storyId
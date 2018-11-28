import random
import time

class ChapterPlayer():
    def __init__(self, storiesManager, speakerManager):
       self.__storiesManager = storiesManager
       self.__speakerManager = speakerManager
    
    #Sequence of colors is empty because it starts a new story
    def startNewStory(self,treeId):
        #Set empty sequence
        self.__sequence = []
        sm = self.__storiesManager
        possibleStories = sm.getStoriesStartingFromTree(treeId)

        storyId = possibleStories[random.randint(0, len(possibleStories))]

        self.__tellChapter(storyId)
        return self.__sequence
    

    #Take color and audiofile of the chapter and reproduce audio
    def __tellChapter(self, storyId):
        chapterId = len(self.__sequence)
        sm = self.__storiesManager
        audioPath = sm.getAudioPath(storyId, chapterId)
        color = sm.getColor(storyId, chapterId)

        self.__sequence.append(color)

        self.__speakerManager.playAudio(audioPath)

        while(self.__speakerManager.get_init() and self.__speakerManager.isPlaying()):
            time.sleep(0.1)
        

    def tellNextChapter(self,sequence):
        #Take sequence from input, sequence = attribute
        self.__sequence = sequence
        storyId = self.__storiesManager.getStoryId(self.__sequence)
        if storyId == -1:
            raise ValueError('Wrong sequence')
        else:
            self.__tellChapter(storyId)
            return self.__sequence


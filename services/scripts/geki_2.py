from geki.GameStates import GameStates
from geki.dots.DotManager import DotManager
from geki.sound.SpeakerManager import SpeakerManager
from geki.StoriesManager import StoriesManager
from geki.dots.DotColor import *
from geki.dots.DotAnimation import *
import random
import geki.config.Constants

class Game():

    def __init__(self, treeId):

        self.__treeId = treeId

        #At the start of the game the state is "NOT_PLAYING"
        self.__gameState = NOT_PLAYING

        #Assign color to a story
        self.__storiesManager = StoriesManager(constants.CONFIG_PATH + "/color_sequences.xml")
        self.__dotManager = DotManager(buttonPressed)
        self.__speakerManager = SpeakerManager() #TODO check parameters
        

    def __startNewStory(self):
        possibleStories = self.__storiesManager.getStoriesStartingAtTree(self.__treeId)
        story_id = possibleStories[random.randInt(0, possibleStories.length)]
        self.__speakerManager.play(StoriesManager.getAudioPath(story_id, 0))
        #TODO continue interaction

    def __askNewGame(self):
        self.__speakerManager.play(constants.STORIES_AUDIO_PATH + "/askNewGame.ogg")
        #and switch on the lights: red for no (odd buttons), green for yes (even buttons)
        i = 0
        for i in dotManager.getDots().length:
            if i % 2 == 0:
                dotManager.setColorAtIndex(i,Colors.GREEN,True)
            else:
                dotManager.setColorAtIndex(i,Colors.RED,True)
            i+=1
        self.gameState = ASKED_IF_NEW_GAME


    def __attractChild(self):
        self.__speakerManager.play(constants.STORIES_AUDIO_PATH + "/attractChild.ogg")
        self.__dotManager.animate(animation=DotAnimation.RAINBOW)

        while(speakerManager.isPlaying()):
            sleep(0.1)
        self.__dotManager.setColor(Colors.OFF) #TODO use specific funcion
        
        #While the child is not playing continuously try to attract the child
        #Stop when the child press the button and change the state from NOT_PLAYING to GAME_STARTED
        while (self.gameState == NOT_PLAYING):
            time.sleep(constants.ATTRACT_WAIT_TIME)
            self.__dotManager.setColor(Colors.WHITE)
            self.__speakerManager.play(constants.STORIES_AUDIO_PATH + "/attractChild.ogg")
            while(speakerManager.isPlaying()):
                sleep(0.1)
            self.__dotManager.setColor(Colors.OFF)
        __askNewGame()

    def buttonPressed(self,index,dot):
        if self.__gameState == NOT_PLAYING:
            self.__gameState = GAME_STARTED
        else :
            if self.__gameState == GAME_STARTED:
                if dot.color.equals(Color.GREEN):
                    self.__gameState = NEW_GAME_STARTED
                    __startNewStory()
                else:
                    if dot.color.equals(Colors.RED):
                        self.__gameState = OLD_GAME_SEQUENCE_ASKED

    def startGame(self):
        __attractChild()

if __name__ == '__main__':
    print("Running")

    treeAttributesManager = treeAttributesManager(constants.CONFIG_PATH)
    treeId = treeAttributesManager.getId()

    game = Game(treeId)
    game.startGame()





    

   
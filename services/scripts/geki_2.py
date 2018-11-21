from geki.GameStates import GameStates
from geki.dots.DotManager import DotManager
from geki.SpeakerManager import SpeakerManager
from geki.StoriesColorManager import StoriesColorManager
from geki.dots.DotColor import *
from geki.dots.DotAnimation import *
import config.constants 

class Game():

    def __init__(self, arg):
        #At the start of the game the state is "NOT_PLAYING"
        self.gameState = NOT_PLAYING

        #Assign color to a story
        self.storiesColorManager = StoriesColorManager(constants.CONFIG_PATH + "/color_sequences.xml")
        self.dotManager = DotManager(buttonPressed)
        self.speakerManager = SpeakerManager() #TODO check parameters
        

    def __startNewStory(self):
        self.speakerManager.play(constants.STORIES_AUDIO_PATH + "/startNewStory.ogg") 

    def __askNewGame(self):
        self.speakerManager.play(constants.STORIES_AUDIO_PATH + "/askNewGame.ogg")
        #and switch on the lights: red for no (odd buttons), green for yes (even buttons)
        i = 0
        for i in dotManager.getDots().length:
            if i % 2 == 0:
                dotManager.setColorAtIndex(i,Colors.GREEN,True)
            else
                dotManager.setColorAtIndex(i,Colors.RED,True)
            i+=1

        self.gameState = ASKED_IF_NEW_GAME


    def __attractChild(self):
        self.speakerManager.play(constants.STORIES_AUDIO_PATH + "/attractChild.ogg")
        self.dotManager.animate(animation=DotAnimation.RAINBOW)

        while(speakerManager.isPlaying())
            sleep(0.1)
        self.dotManager.setColor(Colors.OFF) #TODO use specific funcion
        
        #While the child is not playing continuously try to attract the child
        #Stop when the child press the button and change the state from NOT_PLAYING to GAME_STARTED
        while (gameState = NOT_PLAYING):
            time.sleep(constants.ATTRACT_WAIT_TIME)
            self.dotManager.setColor(Colors.WHITE)
            self.speakerManager.play(constants.STORIES_AUDIO_PATH + "/attractChild.ogg")
            while(speakerManager.isPlaying())
                sleep(0.1)
            self.dotManager.setColor(Colors.OFF)
        __askNewGame()

    def buttonPressed(self,index,dot):
        if self.gameState == NOT_PLAYING:
            self.gameState = GAME_STARTED
        else if self.gameState == GAME_STARTED
            if dot.color.equals(Color.GREEN)
                self.gameState = NEW_GAME_STARTED
                __startNewStory()
            else if dot.color.equals(Colors.RED)
                self.gameState = OLD_GAME_SEQUENCE_ASKED

    def startGame(self):
        __attractChild()

if __name__ == '__main__':
    print("Running")

    game = Game()
    game.startGame()





    

   
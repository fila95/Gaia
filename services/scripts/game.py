import geki.config.Constants as Constants
import random
import signal
import time

from geki.GameStates import GameStates
from geki.StoriesManager import StoriesManager
from geki.TreeAttributesManager import TreeAttributesManager
from geki.dots.DotAnimation import *
from geki.dots.DotColor import *
from geki.dots.DotManager import DotManager
from geki.sound.SpeakerManager import SpeakerManager


class Game():

    def __init__(self, treeId):

        self.__treeId = treeId

        # Assign color to a story
        path = Constants.CONFIG_PATH + "/color_sequences.xml"
        self.__storiesManager = StoriesManager(path)
        self.__dotManager = DotManager(self.dotHasBeenPressed)
        self.__speakerManager = SpeakerManager()  # TODO check parameters

    def __showSequence(self):
        self.__dotManager.turnAllOff()
        self.__gameState = GameStates.SHOWING_SEQUENCE

        if self.__sequence:
            color = self.__sequence[0]
            self.__dotManager.setColorAtIndex(idx=0, color=color)
        else:
            self.__gameState = GameStates.GAME_ENDED

    def __tellChapter(self, storyId):
        chapterId = self.__sequence.length
        sm = self.__storiesManager
        audioPath = sm.getAudioPath(storyId, chapterId)
        color = sm.getColor(storyId, chapterId)

        self.__sequence.append(color)

        self.__speakerManager.playAudio(audioPath)

        while(self.__speakerManager.get_init() and self.__speakerManager.isPlaying()):
            time.sleep(0.1)
        # When the story is finished, the sequence is showed
        self.__showSequence()

    def __startNewStory(self):
        self.__sequence = []
        sm = self.__storiesManager
        possibleStories = sm.getStoriesStartingFromTree(self.__treeId)

        storyId = possibleStories[random.randInt(0, possibleStories.length)]

        self.__tellChapter(storyId)

    def __tellNextChapter():
        storyId = self.__storiesManager.getStoryId(self.__sequence)
        if storyId == -1:
            self.__gameState = GameStates.ASKING_SEQUENCE
            self.__askSequence()
        else:
            self.__tellChapter(storyId)

    def __askSequence():
        path = Constants.AUDIO_PATH + "/askSequence.ogg"
        self.__speakerManager.playAudio(path)

        self.__sequence = []
        self.__gameState = GameStates.GETTING_SEQUENCE

    def __askNewGame(self):
        # and switch on the lights: red for no (odd buttons),
        # green for yes (even buttons)
        i = 0
        for i in dotManager.getDots().length:
            if i % 2 == 0:
                dotManager.setColorAtIndex(i, Colors.GREEN, True)
            else:
                dotManager.setColorAtIndex(i, Colors.RED, True)
            i += 1

        path = Constants.AUDIO_PATH + "/askNewGame.ogg"
        self.__speakerManager.playAudio(path)

    def __attractChild(self):
        path = Constants.AUDIO_PATH + "/attractChild.ogg"
        self.__speakerManager.playAudio(path)
        self.__dotManager.animate(animation=DotAnimation.RAINBOW)

        while (self.__speakerManager.get_init() and self.__speakerManager.isPlaying()):
            continue
        self.__dotManager.turnAllOff()  # TODO use specific funcion

        # While the child is not playing continuously try to attract the child
        # Stop when the child press the button and change
        # the state from NOT_PLAYING to GAME_STARTED
        while (self.__gameState.equals(GameStates.ATTRACTING_CHILD)):
            time.sleep(Constants.ATTRACT_WAIT_TIME)
            if (self.__gameState.equals(GameStates.ATTRACTING_CHILD)):
                self.__dotManager.animate(animation=DotAnimation.RAINBOW)
                self.__speakerManager.playAudio(path)
                while (self.__speakerManager.get_init() and self.__speakerManager.isPlaying()):
                    time.sleep(0.1)
                self.__dotManager.setColor(Colors.OFF)

    def dotHasBeenPressed(self, index, dot):
        if self.__gameState.equals(GameStates.ATTRACTING_CHILD):
            self.__speakerManager.stop()
            self.__gameState = GameStates.ASKING_IF_NEW_GAME
            self.__askNewGame()
        elif self.__gameState.equals(GameStates.ASKING_IF_NEW_GAME):
            if dot.color.equals(Color.GREEN):
                self.__gameState = GameStates.STARTING_NEW_STORY
                self.__startNewStory()
            elif dot.color.equals(Colors.RED):
                self.__gameState = GameStates.ASKING_SEQUENCE
                self.__askSequence()
            else:
                # TODO handle unexpected color
                pass
        elif self.__gameState.equals(GameStates.SHOWING_SEQUENCE):
            color = self.__sequence[0]
            if (color.equals(dot.getColor())):
                self.__sequence.pop()
                self.__dotManager.setColorAtIndex(idx=index, color=Color.OFF)
                self.__showSequence()
        elif self.__gameState.equals(GameStates.GETTING_SEQUENCE):
            color = dot.getColor()
            if color.equals(Colors.WHITE):
                self.__gameState = GameStates.TELLING_NEXT_CHAPTER
                self.__tellNextChapter()
            else:
                self.__sequence.append(dot.getColor())

    def playGame(self):
        # At the start of the game the state is "ATTRACTING_CHILD"
        self.__gameState = GameStates.ATTRACTING_CHILD

        self.__attractChild()

        # avoids restart of the game if it has not finished
        while (not self.__gameState.equals(GameStates.GAME_ENDED)):
            time.sleep(0.1)

    def exit(self):
        if(self.__speakerManager.get_init()):
            self.__speakerManager.stop()
            while(self.__speakerManager.isPlaying()):
                continue
        self.__speakerManager.quit()
        self.__gameState = GameStates.GAME_ENDED
        self.__dotManager.turnAllOff()


def handler(signum, frame):
    print('\nYou pressed ^C. The program is quitting\n')
    global flag
    flag = True
    global game
    game.exit()


if __name__ == '__main__':
    print("Running")
    print("Press ^C to exit\n")
    global flag
    flag = False

    signal.signal(signal.SIGINT, handler)

    while(not flag):
        path = Constants.CONFIG_PATH + "/tree_attributes.xml"
        treeAttribsManager = TreeAttributesManager(path)
        treeId = treeAttribsManager.getId()

        global game
        game = Game(treeId)
        game.playGame()

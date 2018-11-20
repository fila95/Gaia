from geki.GameStates import GameStates
from geki.DotManager import DotManager
from geki.SpeakerManager import SpeakerManager
from geki.StoriesColorManager import StoriesColorManager
from geki.DotColor import Colors
import config.constants 

#variables
global gameState


def buttonPressed():
    if gameState == NOT_PLAYING:
        gameState = GAME_STARTED
        

if __name__ == '__main__':

    print("Running")
    gameState = NOT_PLAYING

    storiesColorManager = StoriesColorManager(constants.CONFIG_PATH + "/color_sequences.xml")
    dotManager = DotManager(buttonPressed)
    speakerManager = SpeakerManager() #TODO check parameters

    dotManager.setColor(Colors.WHITE)
    speakerManager.play(constants.STORIES_AUDIO_PATH + "/attractChild.ogg")
    while(speakerManager.isPlaying())
        sleep(0.1)
    dotManager.setColor(Colors.OFF)

    while (gameState = NOT_PLAYING):
        time.sleep(constants.ATTRACT_WAIT_TIME)
        dotManager.setColor(Colors.WHITE)
        speakerManager.play(constants.STORIES_AUDIO_PATH + "/attractChild.ogg")
        while(speakerManager.isPlaying())
            sleep(0.1)
        dotManager.setColor(Colors.OFF)



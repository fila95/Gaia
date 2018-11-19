from geki.GameStates import GameStates
from geki.DotManager import DotManager
from geki.SpeakerManager import SpeakerManager
from geki.DotColor import Colors

#constants
global stories_audio_path
global config_path
global attract_wait_time

global gameState


def buttonPressed():
    if gameState == NOT_PLAYING:
        gameState = GAME_STARTED
        

stories_audio_path = "resources/audio"
config_path = "config"
attract_wait_time = 10


if __name__ == '__main__':

    print("Running")
    gameState = NOT_PLAYING

    storiesColorManager = StoriesColorManager(path + "/color_sequences.xml")
    dotManager = DotManager(buttonPressed)
    speakerManager = SpeakerManager() #TODO check parameters

    dotManager.setColor(Colors.WHITE)
    speakerManager.play(stories_audio_path + "/attractChild.ogg")
    while(speakerManager.isPlaying())
        sleep(0.1)
    dotManager.setColor(Colors.OFF)

    while (gameState = NOT_PLAYING):
        time.sleep(attract_wait_time)
        dotManager.setColor(Colors.WHITE)
        speakerManager.play(stories_audio_path + "/attractChild.ogg")
        while(speakerManager.isPlaying())
            sleep(0.1)
        dotManager.setColor(Colors.OFF)



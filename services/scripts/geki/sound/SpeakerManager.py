import pygame
from pygame import mixer


class SpeakerManager:

    __speaker = mixer

    def __init__(self):

        # initialize the speaker
        self.__speaker.pre_init(frequency=44100, channels=1)
        pygame.init()
        pygame.mixer.init()
        self.__speaker.music.set_volume(0.1)

    def quit(self):
        print(self.__speaker.get_num_channels())
        print(self.__speaker.get_busy())
        pygame.mixer.set_num_channels(0)
        print(self.__speaker.get_num_channels())
        pygame.mixer.quit()
        pygame.quit()

    def get_init(self):
        self.__speaker.get_init()

    def stop(self):
        self.__speaker.music.stop()

    def pause(self):
        self.__speaker.music.pause()

    def playAudio(self, path=None):
        if self.__speaker.music is not None:
            if path is None:
                self.__speaker.music.unpause()
            else:
                self.__speaker.music.load(path)
                self.__speaker.music.play()

    def setVolume(self, volume):
        if type(volume) is float:
            self.__speaker.music.set_volume(volume)

    def isPlaying(self):
        return self.__speaker.music.get_busy()

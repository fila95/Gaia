import pygame
from pygame import mixer


class SpeakerManager:

    __speaker = mixer

    def __init__(self):

        # initialize the speaker
        self.__speaker.init()
        self.setVolume(1.0)

    def get_init(self):
        return self.get_init()

    def deinit(self):
        self.__speaker.quit()

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

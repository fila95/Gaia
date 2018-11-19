from pygame import mixer

class SystemSoundManager:

    sound = mixer()
    channel = None

    def __init__(self):
        self.__sound.init()
        self.__channel = self.__sound.find_channel()

    def playAudio(self, path=None):
        if self.__channel is not None:
            if path is None:
                self.__channel.unpause()
            else:
                track = self.__sound.Sound(path)
                self.__channel.play(track)

    def stop(self):
        self.__channel.stop()

    def pause(self):
        self.__channel.pause()

    def setVolume(self, volume):
        if type(volume) is float:
            self.__channel.set_volume(volume)

    def isPlaying(self):
        return self.__channel.get_busy()

import threading
import time
from queue import Queue

import pygame
from pygame import mixer


class SpeakerManager:

    __speaker = mixer

    def __init__(self, finishPlayingCallback):

        # initialize the speaker
        self.__finishPlayingCallback = finishPlayingCallback
        self.__speaker.init()
        self.setVolume(1.0)
        self.queue = Queue()
        self.interrupt_event = threading.Event()


    def deinit(self):
        self.__speaker.quit()

    def stop(self):
        self.__speaker.music.stop()
        self.interrupt_event.set()

    def pause(self):
        self.__speaker.music.pause()
        self.interrupt_event.set()

    def resume(self):
        self.__speaker.music.unpause()
        self.__handle_async(self.__checkPlaying, False)

    def playAudio(self, path):
        if self.isPlaying:
            self.stop()

        self.__speaker.music.load(path)
        self.__speaker.music.play()
        self.__handle_async(self.__checkPlaying, False)

    def setVolume(self, volume):
        if type(volume) is float:
            self.__speaker.music.set_volume(volume)

    def isPlaying(self):
        return self.__speaker.music.get_busy()


    def __handle_async(self, lfunc, interrupt=True):
        # ql = self.queue.qsize()
        if (interrupt == True and not self.queue.empty() and not self.interrupt_event.isSet()):
            self.interrupt_event.set()
        self.queue.put(lfunc)

    def __checkPlaying(self):
        while self.isPlaying():
            time.sleep(0.1)
        self.__finishPlayingCallback()
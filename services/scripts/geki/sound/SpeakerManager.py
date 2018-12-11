import threading
import time
from queue import Queue
from .SpeakerWorker import SpeakerWorker

import logging

import pygame
from pygame import mixer


class SpeakerManager:

	__speaker = mixer

	def __init__(self, finishPlayingCallback):

		# initialize the speaker
		self.__finishPlayingCallback = finishPlayingCallback
		self.__speaker.init()
		self.setVolume(1.0)

		self.__queue = Queue()
		self.__interrupt_event = threading.Event()
		self.__stop_event = threading.Event()

		self.__worker = SpeakerWorker(logging, self.__queue, self.__stop_event, self.__interrupt_event)
		self.__worker.start()

		self.callsCallbackWhenInterrupted = False


	def deinit(self):
		self.__speaker.quit()

	def stop(self):
		self.__speaker.music.stop()
		self.__interrupt_event.set()

	def pause(self):
		self.__speaker.music.pause()
		self.__interrupt_event.set()

	def resume(self):
		self.__speaker.music.unpause()
		self.__handle_async(self.__checkPlaying, False)

	def playAudio(self, path):
		print("Playing audio file at path {}".format(path))
		if self.isPlaying():
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
		if (interrupt == True and not self.__queue.empty() and not self.__interrupt_event.isSet()):
			self.__interrupt_event.set()
		self.__queue.put(lfunc)

	def __checkPlaying(self):
		interrupt = False
		print("checking")
		while self.__speaker.music.get_busy() and not interrupt:
			interrupt = self.__interrupt_event.isSet()
			time.sleep(0.1)
		print("checked")
		if not interrupt or self.callsCallbackWhenInterrupted:
			self.__playingFinished()


	def __playingFinished(self):
		print("SpeakerManager finished playing!")
		self.__finishPlayingCallback()
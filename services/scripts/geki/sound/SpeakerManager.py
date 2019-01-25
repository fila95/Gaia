import threading
import time
from queue import Queue
from .SpeakerWorker import SpeakerWorker

import logging

from omxplayer import OMXPlayer


class SpeakerManager:

	def __init__(self, finishPlayingCallback):

		# initialize the speaker
		self.__finishPlayingCallback = finishPlayingCallback
		self.player = None

		self.__queue = Queue()
		self.__interrupt_event = threading.Event()
		self.__stop_event = threading.Event()

		self.__worker = SpeakerWorker(logging, self.__queue, self.__stop_event, self.__interrupt_event)
		self.__worker.start()

		self.callsCallbackWhenInterrupted = False


	def deinit(self):
		self.stop()

	def stop(self):
		if self.player is not None or self.isPlaying():
			try:
				self.player.quit()
			except:
				pass
		self.player = None

	def playAudio(self, path):
		print("Playing audio file at path {}".format(path))
		if self.isPlaying():
			self.stop()
		
		self.player = OMXPlayer(source=path, args=['-o', 'local'])
		self.player.stopEvent += lambda event: self.__playingFinished()
		self.player.play()
		self.__handle_async(self.__checkPlaying, False)


	def setVolume(self, volume):
		pass

	def isPlaying(self):
		if self.player is None:
			return False

		playing = False
		try:
			playing = self.player.playback_status() == "Playing"
		except:
			playing = False

		return playing


	def __handle_async(self, lfunc, interrupt=True):
		# ql = self.queue.qsize()
		if (interrupt == True and not self.__queue.empty() and not self.__interrupt_event.isSet()):
			self.__interrupt_event.set()
		self.__queue.put(lfunc)

	def __checkPlaying(self):
		interrupt = False
		# print("checking")
		while self.isPlaying() and not interrupt:
			interrupt = self.__interrupt_event.isSet()
			time.sleep(0.1)
		# print("checked")
		if not interrupt or self.callsCallbackWhenInterrupted:
			self.__playingFinished()


	def __playingFinished(self):
		print("SpeakerManager finished playing!")
		self.stop()
		self.__finishPlayingCallback()
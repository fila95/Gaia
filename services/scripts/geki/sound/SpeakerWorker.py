import threading
from queue import Queue, Empty

class SpeakerWorker(threading.Thread):
	"""
	Simple Worker that can execute any lambda function via a Queue
	If the function has the same "interrupt-event" it can be interrupted by setting the flag
	"""
	def __init__(self, logger, queue, stop_event, interrupt_event):
		threading.Thread.__init__(self)
		self.daemon = True
		self.queue = queue
		self.stop_event = stop_event
		self.interrupt_event = interrupt_event
		self._logger = logger

	def run(self):
		self._logger.info("Running worker")
		while True and not self.stop_event.isSet():
			try:
				func = self.queue.get(block=True, timeout=2)
				self._logger.info("Worker got work!")
				func()
				self.queue.task_done()
				self.interrupt_event.clear()
			except Empty:
				pass
			except TypeError as e:
				self._logger.info(str(e))
		self._logger.info("Audio worker DONE")
from Game import Game

import asyncio
import sys


loop = None

if __name__ == '__main__':
	try:
		game = Game()
		game.start()

		# run the event loop
		loop = asyncio.get_event_loop()
		loop.run_forever()
		loop.close()

	except:
		game.stop()
		print("Error:", sys.exc_info()[0])

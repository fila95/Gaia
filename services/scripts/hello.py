import asyncio
import sys


if __name__ == '__main__':
	try:
		print("Hello")

		# run the event loop
		loop = asyncio.get_event_loop()
		loop.run_forever()
		loop.close()

	except:
		print("Error:", sys.exc_info()[0])

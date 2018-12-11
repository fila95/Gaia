from dots import DotManager
from dots import DotAnimation
from dots import DotColor, Colors
from dots import Dot

import asyncio
import sys

def dotWasTapped(index, dot):
	
	print("Tapped Dot at index: ", end="", flush=True)
	print(index)
	if (index == 0):
		manager.setAnimationAffectDots(dotWasTapped.animationAffectDots)
		dotWasTapped.animationAffectDots = not dotWasTapped.animationAffectDots
		manager.animate(animation=DotAnimation.RAINBOW_CYCLE, keep_running=True)
	else:
		for i in range(manager.getDotsCount()):
			manager.setColorAtIndex(i, Colors.random(), fade=True)
			
dotWasTapped.animationAffectDots = True

loop = None
manager = DotManager(tapHandler=dotWasTapped)

if __name__ == '__main__':
	try:
		# manager.setColor(Colors.random(), fade=False)
		# manager.setBrightness(255, fade=False)
		manager.animate(animation=DotAnimation.RAINBOW_CYCLE, keep_running=True)

		# run the event loop
		loop = asyncio.get_event_loop()
		loop.run_forever()
		loop.close()

	except:
		print("Error:", sys.exc_info()[0])

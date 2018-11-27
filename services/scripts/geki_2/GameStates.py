from enum import Enum

class GameStates(Enum):
    
    IDLE=0
    WAITING_SEQUENCE=1
    TELLING_STORY=2
    ENDING=3

    def equals(self, gameState):
        return self.value == gameState.value

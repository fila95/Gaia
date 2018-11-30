from enum import Enum

class GameStates(Enum):
    
    IDLE=0
    WAITING_FIRST_CONTACT=1
    WAITING_SEQUENCE=2
    TELLING_STORY=3
    ENDING=4

    def equals(self, gameState):
        return self.value == gameState.value

    def waitTime(self):
        if self == GameStates.WAITING_FIRST_CONTACT:
            return 5
        elif self == GameStates.WAITING_SEQUENCE:
            return 1
        elif self == GameStates.ENDING:
            return 5
        else:
            return 0

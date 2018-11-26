from enum import Enum


class GameStates(Enum):
    ATTRACTING_CHILD = 1
    ASKING_IF_NEW_GAME = 2
    STARTING_NEW_STORY = 3
    ASKING_SEQUENCE = 4
    GETTING_SEQUENCE = 5
    TELLING_NEXT_CHAPTER = 6
    SHOWING_SEQUENCE = 7
    GAME_ENDED = 0

    def equals(self, gameState):
        return self.value == gameState.value

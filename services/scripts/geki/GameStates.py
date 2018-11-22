from enum import Enum

class GameStates(Enum):
    NOT_PLAYING = 1
    GAME_STARTED = 2
    ASKED_IF_NEW_GAME = 3
    NEW_GAME_STARTED = 4
    OLD_GAME_SEQUENCE_ASKED = 5
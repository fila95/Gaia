import json

from services.scripts.geki_2.dots import DotColor


class Story:

    __name = ''
    __colorSequence = []
    __path = []
    __color = []

    def __init__(self, name, colors=[], paths=[]):

        self.__name = name
        self.__colorSequence = colors
        self.__path = paths

    def getName(self):
        return self.__name

    def chapterPath(self, index=0):

            if index >= len(self.__path):
                return self.__path[index]

    def checkSequence(self, sequence=[]):

        if len(sequence) <= len(self.__colorSequence):
            for i in range(0, len(sequence)):
                if not self.__colorSequence[i].equals(sequence[i]):
                    return False
            return True
        return False

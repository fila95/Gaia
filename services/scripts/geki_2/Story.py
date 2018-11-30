import json

from dots import DotColor


class Story:

    __name = ''
    __colorSequence = []
    __path = []
    __lastElement = False

    def __init__(self, name, colors=[], paths=[]):

        self.__name = name
        self.__colorSequence = colors
        self.__path = paths

    def getName(self):
        return self.__name

    def chapterPath(self, colorSequence=[]):
            if len(colorSequence) <= len(self.__path):
                return self.__path[len(colorSequence)-1]

    def checkSequence(self, sequence=[]):
        if len(sequence) <= len(self.__colorSequence):
            for i in range(0, len(sequence)):
                if not self.__colorSequence[i].equals(sequence[i]):
                    return False

            return True
        return False

    def nextSequence(self, sequence=[]):
        if len(sequence) < len(self.__colorSequence):
            sequence.append(self.__colorSequence[len(sequence)])
            return sequence
        return None

    def isLastChapter(self, sequence=[]):
        if len(sequence) == len(self.__colorSequence):
            return True
        return False
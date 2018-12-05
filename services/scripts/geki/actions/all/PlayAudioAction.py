from ..Action import Action
from ..utils.Story import Story


class StoriesPickerAction(Action):

    @staticmethod
    def parseIdentifier():
        return 'PLAY_AUDIO'

    def __init__(self, data):
        super().__init__(data)
        ## Parse attributes
        if "path" in data:
            self.path = data["path"]

    def startAction(self, optionalParams=None):
        if optionalParams is not None:
            if "path" in  optionalParams:
                self.path = optionalParams["path"]

        if self.path is not None:
            self.speakerManager.playAudio(self.path)

    def deactivate(self):
        pass

    def audioDidFinishPlaying(self):
        self.nextAction()

    def dotWasTapped(self, index, dot):
        pass

    def timerFired(self):
        pass


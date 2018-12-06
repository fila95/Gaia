from ..Action import Action


class SingleChoiceMenuAction(Action):

    @staticmethod
    def parseIdentifier():
        return 'SINGLE_CHOICE_MENU'

    def __init__(self, data):
        super().__init__(data)
        ## Parse attributes

        self.colors = []
        self.actions = []

        from dots.DotColor import DotColor
        for opt in data["options"]:
            self.colors.append(DotColor(red=opt["color"]["red"], green=opt["color"]["green"], blue=opt["color"]["blue"]))
            self.actions.append(opt["actions"])

        self.timeoutActions = self.parseActionsFromJson(data["timeout_actions"])



    def startAction(self, optionalParams=None):
        self.dotManager.setColors(colors=self.colors, fade=True)

        if self.timeout is not None:
            self.scheduleTimer(duration=self.timeout)

    def deactivate(self):
        pass

    def audioDidFinishPlaying(self):
        pass

    def dotWasTapped(self, index, dot):
        self.produceActions(self.actions[index])
        self.nextAction()

    def timerFired(self):
        self.produceActions(self.timeoutActions)
        self.nextAction()
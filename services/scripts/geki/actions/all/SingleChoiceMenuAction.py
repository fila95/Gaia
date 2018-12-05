from ..Action import Action


class SingleChoiceMenuAction(Action):

    @staticmethod
    def parseIdentifier():
        return 'SINGLE_CHOICE_MENU'

    def __init__(self, data):
        super().__init__(data)
        ## Parse attributes

        self.actionToExecute = None
        self.rightColor = None
        self.allColor = []
        self.repeatColor = False
        self.wrongChoice = None


        if "repeat_colors_if_needed" in data:
            self.repeatColor = data["repeat_colors_if_needed"]

        from dots.DotColor import DotColor
        option = data["option"]


        self.rightColor = DotColor(option["red"], option["green"], option["blue"])
        self.allColor.append(self.rightColor)

        self.actionToExecute = self.parseSingleAction(option["action"])

        if "additional_colors" in data:
            additionalColor = data["additional_colors"]
            for color in additionalColor["colors"]:
                self.allColor.append(DotColor(color["red"], color["green"], color["blue"]))


        self.wrongChoice = self.parseSingleAction(data["wrong_choice"])


    def startAction(self, optionalParams=None):
        if len(self.allColor) == self.dotManager.getDotsCount():
            self.dotManager.setColors(self.allColor, fade=True)
        elif self.repeatColor:
            for count in range(0, (len(self.allColor) - self.dotManager.getDotsCount())):
                color = self.allColor[count]
                self.allColor.append(color)
            self.dotManager.setColors(self.allColor, fade=True)
        else:
            from dots.DotColor import Colors
            for count in range(0, (len(self.allColor) - self.dotManager.getDotsCount())):
                color = Colors.random()
                self.allColor.append(color)
            self.dotManager.setColors(self.allColor, fade=True)

        if self.timeout is not None:
            self.scheduleTimer(duration=self.timeout)

    def deactivate(self):
        pass

    def audioDidFinishPlaying(self):
        pass

    def dotWasTapped(self, index, dot):
        if self.rightColor.equals(dot.getColor()):
            self.produceActions([self.actionToExecute])
            self.nextAction()
        else:
            pass
            self.produceActions([self.wrongChoice])
            self.nextAction()

    def timerFired(self):
        self.nextAction()
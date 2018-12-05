from ..Action import Action


class CombinedAction(Action):

    @staticmethod
    def parseIdentifier():
        return 'COMBINED'

    def __init__(self, data):
        super().__init__(data)
        ## Parse attributes

        self.actions = self.parseActionsFromJson(data["actions"])
        filtered = []
        for a in self.actions:
            if a._excludedInCombinedActions == False:
                filtered.append(a)
        self.actions = filtered

        self.policy = data["policy"]



    ## Overrides
    def startAction(self, optionalParams=None):
        if len(self.actions) == 0:
            self.nextAction()
        else:
            for a in self.actions:
                a._activate(game=self._game)
            self.__check()

    def deactivate(self):
        for a in self.actions:
            a._deactivate()

    def audioDidFinishPlaying(self):
        for a in self.actions:
            a.audioDidFinishPlaying()
        self.__check()

    def dotWasTapped(self, index, dot):
        for a in self.actions:
            a.dotWasTapped(index, dot)
        self.__check()

    def timerFired(self):
        if self.policy == "EXIT_TIMEOUT":
            self.nextAction()

    def __check(self):
        from ..Action import ActionState

        if self.policy == "WAIT_ALL":
            canExit = True
            for a in self.actions:
                if a.state == ActionState.IDLE or a.state == ActionState.STARTED:
                    canExit = False
                    break

            if canExit:
                self.nextAction()
                return

        if self.policy == "WAIT_FIRST":
            canExit = False
            for a in self.actions:
                if a.state == ActionState.ENDED:
                    canExit = True
                    break

            if canExit:
                self.nextAction()
                return

        # if self.policy == "EXIT_TIMEOUT":
        #     pass

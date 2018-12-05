from ..Action import Action


class ConcurrentAction(Action):

    @staticmethod
    def parseIdentifier():
        return 'CONCURRENT'

    def __init__(self, data):
        super().__init__(data)
        ## Parse attributes

        self.identifierList = []
        self.actions = []

        
        for action in data["actions"]:
            self.identifierList.append((action["parserIdentifier"]))
            self.actions.append(action["path"])


        self.policy = data["policy"]
        self.timeout = data["timeOut"]

    def startAction(self, optionalParams=None):

        self.concurrentAction = []
        for action in self.actions:
            self.concurrentAction.append(self.parseActionsFromFile(filename=action))
        self.numberOfAction = len(self.concurrentAction)

        self.scheduleTimer(duration=self.timeout)


    def deactivate(self):
        pass

    def audioDidFinishPlaying(self):

        if self.policy == "WAIT_FIRST":
            self.nextAction()
        elif self.policy == "WAIT_ALL":
            self.numberOfAction = self.numberOfAction-1
            if self.numberOfAction == 0:
                self.nextAction()

    def dotWasTapped(self, index, dot):
        if self.policy == "WAIT_FIRST":
            self.nextAction()
        elif self.policy == "WAIT_ALL":
            self.numberOfAction = self.numberOfAction-1
            if self.numberOfAction == 0:
                self.nextAction()

    def timerFired(self):
        self.nextAction()
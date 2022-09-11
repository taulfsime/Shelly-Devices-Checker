class Action:
    CanNotReach = "CanNotReach"
    CheckVar = "CheckVar"
    EachCheck = "EachCheck"

    def __init__(self, data):
        self.data = data
        self.when = self.data["when"]
        self.do = self.data["do"]
        self.enabled = self.data["enabled"]

        self.handlers = {
            self.CanNotReach: self._canNotReachHandler,
            self.CheckVar: self._checkVariableHandler,
            self.EachCheck: self._OnEachCheckHandler
        }

    def _canNotReachHandler(self, targetData):
        if not self.enabled: return

        if self.when["type"].lower() == self.CanNotReach.lower():
            if self.when["target"] == targetData["ip"]:
                self.execute(targetData)

    def _OnEachCheckHandler(self, targetData):
        if not self.enabled: return

        if self.when["type"].lower() == self.EachCheck.lower():
            self.execute(targetData)

    def _checkVariableHandler(self, targetData):
        if not self.enabled: return

        if self.when["type"].lower() == self.CheckVar.lower():
            if self.when["target"] == targetData["ip"] and self.when["var"] in targetData:
                targetValue = targetData[self.when["var"]]
                checkValue = self.when["value"]

                if self.when["check"] == "lower":
                    if targetValue < checkValue:
                        self.execute(targetData)

                elif self.when["check"] == "equal":
                    if targetValue == checkValue:
                        self.execute(targetData)

                elif self.when["check"] == "higher":
                    if targetValue > checkValue:
                        self.execute(targetData)
                    

    def _callUrl(self, action, targetData):
        if "url" not in action:
            raise Exception("Missing parameter: URL")

        import requests
        ret = requests.get(action["url"])

    def _consoleLog(self, action, targetData):
        print(targetData)

    def check(self, event, targetData):
        if not self.enabled: return
    
        if event in self.handlers:
            self.handlers[event](targetData)

    def execute(self, targetData = None):
        for action in self.do:
            if action["type"].lower() == "callUrl".lower():
                self._callUrl(action, targetData)
            elif action["type"].lower() == "consoleLog".lower():
                self._consoleLog(action, targetData)

class ActionsList:
    def __init__(self, data):
        self.data = data
        self.actions = [Action(x) for x in self.data]

    def checkHandler(self, event, targetData):
        for act in self.actions:
            act.check(event, targetData)
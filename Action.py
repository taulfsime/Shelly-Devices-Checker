class Action:
    CanNotReach = "CanNotReach"
    CheckVar = "CheckVar"

    def __init__(self, data):
        self.data = data
        self.when = self.data["when"]
        self.do = self.data["do"]
        self.enabled = self.data["enabled"]

        self.handlers = {
            self.CanNotReach: self._canNotReachHandler,
            self.CheckVar: self._checkVariableHandler
        }

    def _canNotReachHandler(self, targetData):
        if not self.enabled: return

        if self.when["type"].lower() == self.CanNotReach.lower():
            if self.when["target"] == targetData["ip"]:
                self.execute()

    def _checkVariableHandler(self, targetData):
        if not self.enabled: return

        if self.when["type"].lower() == self.CheckVar.lower():
            if self.when["target"] == targetData["ip"] and self.when["var"] in targetData:
                targetValue = targetData[self.when["var"]]
                checkValue = self.when["value"]

                if self.when["check"] == "lower":
                    if targetValue < checkValue:
                        self.execute()

                elif self.when["check"] == "equal":
                    if targetValue == checkValue:
                        self.execute()

                elif self.when["check"] == "higher":
                    if targetValue > checkValue:
                        self.execute()
                    

    def _callUrl(self, action):
        if "url" not in action:
            raise Exception("Missing parameter: URL")

        import requests
        ret = requests.get(action["url"])

    def check(self, event, targetData):
        if not self.enabled: return
    
        if event in self.handlers:
            self.handlers[event](targetData)


    def execute(self):
        for action in self.do:
            if action["type"].lower() == "callUrl".lower():
                self._callUrl(action)

class ActionsList:
    def __init__(self, data):
        self.data = data
        self.actions = [Action(x) for x in self.data]

    def checkHandler(self, event, targetData):
        for act in self.actions:
            act.check(event, targetData)
class ConditionTypes:
    CanNotReach = "CanNotReach"
    CheckVar = "CheckVar"
    EachCheck = "EachCheck"

class ActionTypes:
    CallUrl = "CallUrl"
    ConsoleLog = "ConsoleLog"

class Webhook:
    def __init__(self, data):
        self.data = data
        self.when = self.data["when"]
        self.do = self.data["do"]
        self.enabled = self.data["enabled"]
        self.eventLogHandler = None

        self.handlers = {
            ConditionTypes.CanNotReach: self._canNotReachHandler,
            ConditionTypes.CheckVar: self._checkVariableHandler,
            ConditionTypes.EachCheck: self._OnEachCheckHandler,
        }

        self.actions = {
            ActionTypes.CallUrl: self._callUrl,
            ActionTypes.ConsoleLog: self._consoleLog,
        }

    def _canNotReachHandler(self, target):
        if self.when["target"] == target.ip:
            self.execute(target)

    def _OnEachCheckHandler(self, target):
        self.execute(target)

    def _checkVariableHandler(self, target):
        if self.when["target"] == target.ip and self.when["var"] in target.commandsList:
            targetValue = target.getValue(self.when["var"])
            checkValue = self.when["value"]

            if self.when["check"] == "lower":
                if targetValue < checkValue:
                    self.execute(target)

            elif self.when["check"] == "equal":
                if targetValue == checkValue:
                    self.execute(target)

            elif self.when["check"] == "higher":
                if targetValue > checkValue:
                    self.execute(target)            

    def _callUrl(self, action, target):
        if "url" not in action:
            raise Exception("Missing parameter: URL")

        import requests
        ret = requests.get(action["url"])

    def _consoleLog(self, action, target):
        print(target)

    def check(self, event, target):
        if not self.enabled: return
    
        if event in self.handlers and event == self.when["type"]:
            self.handlers[event](target)

    def execute(self, target = None):
        for action in self.do:
            if action["type"] in self.actions:
                self.actions[action["type"]](action, target)

    def setEventLogHandler(self, handler):
        self.eventLogHandler = handler
class ConditionTypes:
    CanNotReach = "CanNotReach"
    CheckVar = "CheckVar"
    EachCheck = "EachCheck"

class ActionTypes:
    CallUrl = "CallUrl"
    ConsoleLog = "ConsoleLog"
    WriteToLog = "WriteToLog"

class WebhooksList:
    def __init__(self, data):
        self.data = data
        self.webhooks = [Webhook(x) for x in self.data]

    def checkHandler(self, event, targetData):
        for act in self.webhooks:
            act.check(event, targetData)

    def setEventLogHandler(self, handler):
        for act in self.webhooks:
            act.setEventLogHandler(handler)

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
            ActionTypes.WriteToLog: self._writeToLog
        }

    def _canNotReachHandler(self, targetData):
        if self.when["target"] == targetData["ip"]:
            self.execute(targetData)

    def _OnEachCheckHandler(self, targetData):
        self.execute(targetData)

    def _checkVariableHandler(self, targetData):
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

    def _writeToLog(self, action, targetData):
        if self.eventLogHandler:
            self.eventLogHandler(targetData)

    def check(self, event, targetData):
        if not self.enabled: return
    
        if event in self.handlers and event == self.when["type"]:
            self.handlers[event](targetData)

    def execute(self, targetData = None):
        for action in self.do:
            if action["type"] in self.actions:
                self.actions[action["type"]](action, targetData)

    def setEventLogHandler(self, handler):
        self.eventLogHandler = handler


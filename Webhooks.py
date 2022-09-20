class WebhookCondition:
    CanNotReach = "CanNotReach"
    CheckVar = "CheckVar"
    OnRefresh = "OnRefresh"

    def __init__(self, data):
        from ShellyDevice import ShellyDevice

        self.data = data
        self.target = ShellyDevice(self.data["target"]) if "target" in self.data else False
        self.andCondition = self.self["and"] if "and" in self.data else False

        self.handlers = {
            self.CanNotReach: self._CanNotReach,
            self.CheckVar: self._CheckVar,
            self.OnRefresh: self._OnRefresh
        }

    """
    {
        "type": "CanNotReach",
        "target": "192.168.000.000"
        "and": {...}
    }
    """
    def _CanNotReach(self) -> bool:
        return not self.target.valid()

    """
    {
        "type": "OnRefresh",
        "target": "000.000.000.000"
        "and": {...}
    }
    """
    def _OnRefresh(self) -> bool:
        return True

    """
    {
        "type": "CheckVar",
        "target": "000.000.000.000"
        "var": "WiFiRSSI",
        "value": -50,
        "compare": "higher" -> Possible values are: higher, lower and equal
    }
    """
    def _CheckVar(self) -> bool:
        var = self.data["var"]
        if var in self.target.commandsList:
            targetValue = self.target.getValue(var)
            checkValue = self.data["value"]

            if self.data["check"] == "lower":
                if targetValue < checkValue:
                    return True
            elif self.data["check"] == "equal":
                if targetValue == checkValue:
                    return True
            elif self.data["check"] == "higher":
                if targetValue > checkValue:
                    return True

        return False

    def check(self):
        self.target.refresh()

        if self.andCondition and not self.andCondition.check():
            return False

        if self.data["type"] in self.handlers:
            return self.handlers[self.data["type"]]()

        return False

    def getTarget(self):
        return self.target

class ActionTypes:
    CallUrl = "CallUrl"
    ConsoleLog = "ConsoleLog"

class Webhook:
    def __init__(self, data):
        self.data = data
        self.conditions = [WebhookCondition(x) for x in self.data["conditions"]]
        self.do = self.data["do"]
        self.enabled = self.data["enabled"]

        self.actions = {
            ActionTypes.CallUrl: self._callUrl,
            ActionTypes.ConsoleLog: self._consoleLog,
        }

    def _callUrl(self, action, target):
        if "url" not in action:
            raise Exception("Missing parameter: URL")

        import requests
        ret = requests.get(action["url"])

    def _consoleLog(self, action, target):
        print(target)

    def performCheck(self) -> None:
        if not self.enabled: return

        for cond in self.conditions:
            if cond.check():
                self.execute(cond.getTarget())

    def execute(self, target = None):
        for action in self.do:
            if action["type"] in self.actions:
                self.actions[action["type"]](action, target)



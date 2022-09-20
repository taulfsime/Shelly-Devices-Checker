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

        self.handlers = {
            ConditionTypes.CanNotReach: self._canNotReachHandler,
            ConditionTypes.CheckVar: self._checkVariableHandler,
            ConditionTypes.EachCheck: self._OnEachCheckHandler,
        }

        self.actions = {
            ActionTypes.CallUrl: self._callUrl,
            ActionTypes.ConsoleLog: self._consoleLog,
        }

    """
    {
        "type": "CanNotReach",
        "target": "192.168.000.000" 
        "and": {...}
    }
    """
    def _canNotReachHandler(self, condition, target) -> bool:
        if "and" in condition and not self._checkcondition(condition, target):
            return False

        if "target" not in self.when or self.when["target"] == target.ip:
            return not target.isValid

        return False

    """
    {
        "type": "EachCheck",
        "and": {...}
    }
    """
    def _OnEachCheckHandler(self, condition, target) -> bool:
        if "and" in condition and not self._checkcondition(condition, target):
            return False

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
    def _checkVariableHandler(self, condition, target) -> bool:
        if "and" in condition and not self._checkCondition(condition, target):
            return False

        if self.when["target"] == target.ip and self.when["var"] in target.commandsList:
            targetValue = target.getValue(self.when["var"])
            checkValue = self.when["value"]

            if self.when["check"] == "lower":
                if targetValue < checkValue:
                    return True

            elif self.when["check"] == "equal":
                if targetValue == checkValue:
                    return True
            elif self.when["check"] == "higher":
                if targetValue > checkValue:
                    return True

        return False

    def _callUrl(self, action, target):
        if "url" not in action:
            raise Exception("Missing parameter: URL")

        import requests
        ret = requests.get(action["url"])

    def _consoleLog(self, action, target):
        print(target)

    def check(self, target) -> None:
        if not self.enabled: return

        for condition in self.when:
            if self._checkCondition(condition, target):
                self.execute(target)

    def _checkCondition(self, condition, target) -> bool:
        if condition["type"] not in self.handlers:
            raise Exception(f"Unknown conditio type ({condition})")

        return self.handlers[condition["type"]](condition, target)

    def execute(self, target = None):
        for action in self.do:
            if action["type"] in self.actions:
                self.actions[action["type"]](action, target)

    def deviceOnRefresh(self, device):
        print(f"REFRESH: {device}")

    def deviceOnInvalid(self, device):
        print(f"INVALID: {device}")

    def getTargets(self):
        return [x["target"] for x in self.when]

    def applyToDevice(self, device):
        if not device.isValid(): return False
        if device.ip not in self.getTargets(): return False

        device.setOnInvalid(self.deviceOnInvalid)
        device.setOnRefresh(self.deviceOnRefresh)

        return True



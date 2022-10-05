class AutomationCondition:
    CanNotReach = "CanNotReach"
    CheckVar = "CheckVar"
    OnRefresh = "OnRefresh"

    def __init__(self, data):
        self.data = data
        self.target = self.data["target"]
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
    def _CanNotReach(self, target) -> bool:
        return not target.valid()

    """
    {
        "type": "OnRefresh",
        "target": "000.000.000.000"
        "and": {...}
    }
    """
    def _OnRefresh(self, traget) -> bool:
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
    def _CheckVar(self, target) -> bool:
        var = self.data["var"]
        if var in target.commandsList:
            targetValue = target.getValue(var)
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

    def check(self, devices):
        if self.andCondition and not self.andCondition.check(devices):
            return False

        if self.data["type"] in self.handlers:
            return self.handlers[self.data["type"]](devices[self.target])

        return False

    def getTargets(self, list = []):
        list.append(self.target)
        if self.andCondition:
            list.append(self.andCondition.getTargets())

        return list

class Automation:
    from ShellyDevice import ShellyDevice
    CallURL = "CallURL"
    ConsoleLog = "ConsoleLog"

    def __init__(self, data):
        self.data = data
        self.conditions = [AutomationCondition(x) for x in self.data["conditions"]]
        self.do = self.data["do"]
        self.enabled = self.data["enabled"]

        self.actions = {
            self.CallURL: self._callURL,
            self.ConsoleLog: self._consoleLog,
        }

    """
    {
        "type": "ConsoleLog",
        "target": "XXX.XXX.XXX.XXX"
    }
    """
    def _consoleLog(self, actionData, target: ShellyDevice, validCondition: AutomationCondition):
        print(validCondition.target)

    """
    {
        "type": "CallURL",
        "URL": "..."
    }
    """
    def _callURL(self, actionData, target: ShellyDevice, validCondition: AutomationCondition):
        import requests
        ret = requests.get(actionData["url"])

    def performCheck(self, devices) -> None:
        if not self.enabled: return

        for cond in self.conditions:
            if cond.check(devices):
                self.execute(devices, cond)
                return #Prevent executing the automation more than a once

    def execute(self, devices, validCondition: AutomationCondition):
        for action in self.do:
            if action["type"] in self.actions:
                target = devices[action["target"]] if "target" in action else None

                self.actions[action["type"]](action, target, validCondition)

    def getTargets(self):
        targets = []

        for cond in self.conditions:
            targets.extend(cond.getTargets())

        for act in self.do:
            if "target" in act:
                targets.append(act["target"])
        
        return targets



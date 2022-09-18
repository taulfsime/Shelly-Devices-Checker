class ConditionTypes:
    CanNotReach = "CanNotReach"
    CheckVar = "CheckVar"
    EachCheck = "EachCheck"

class ActionTypes:
    CallUrl = "CallUrl"
    ConsoleLog = "ConsoleLog"
"""
    Rename to Action
    Each action can containes multiple actions (can be seperated in classes)
    Each action has single or multiple conditions (seperated in objects)
    Check function that will loop over every condition and change its 'shouldExecute' value on true or false
    Condition can has "and" object which will be called also, if the main parrent condition is true
    If more than one conditions are valid execute all actions
    Actions should have call function that will execute the action without checking the conditions

    Good to have:
    feedback for each 'and' object
"""
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
        "target": "192.168.000.000" -> if missing execute on every call
    }
    """
    def _canNotReachHandler(self, target):
        if self.when["target"] == target.ip:
            self.execute(target)

    """
    {
        "type": "EachCheck"
    }
    """
    def _OnEachCheckHandler(self, target):
        self.execute(target)

    """
    {
        "type": "CheckVar",
        "target": "000.000.000.000" -> If missing checkes every call
        "var": "WiFiRSSI",
        "value": -50,
        "compare": "higher" -> Possible values are: higher, lower and equal
    }
    """
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
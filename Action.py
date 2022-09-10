class Action:
    def __init__(self, data):
        self.data = data
        self.when = self.data["when"]
        self.do = self.data["do"]
        self.enabled = self.data["enabled"]

    def CanNotReachHandler(self, target):
        if not self.enabled: return

        if self.when["type"].lower() == "CanNotReach".lower():
            if self.when["target"] == target:
                self.execute()

    def CheckVariableHandler(self, target, targetData):
        if not self.enabled: return

        if self.when["type"].lower() == "CheckVar".lower():
            if self.when["target"] == target and self.when["var"] in targetData:
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

    def execute(self):
        for action in self.do:
            if action["action"].lower() == "callUrl".lower():
                self._callUrl(action)
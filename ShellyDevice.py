class ShellyDevice:
    DEVICES = {
        "SHSW-PM": "Shelly1PM",
        "SHUNI-1": "ShellyUNI"
    }

    def __init__(self, ip, onFail = None, onRefresh = None):
        self.ip = ip
        self.onRefresh = onRefresh
        self.onFail = onFail
        self.commands = {}
        self.commandsList = []
        self.data = {}
        self.prevData = {}

        self._fetchDeviceGen()
        self.refresh()
        self._loadKeys()

    def refresh(self):
        self.isValid = True
        
        self.prevData = self.data

        self._fetchStatus()
        self._fetchConfig()

        if self.onRefresh:
            self.onRefresh(self)

    def getChanged(self):
        if len(self.data) == 0 or len(self.prevData) == 0:
            return False
        
        changed = {}
        for key in self.commandsList:
            curr = self.getValue(key)
            prev = self.getPrevValue(key)

            print(f"{key} {prev} {curr}")

            if curr != prev:
                changed[key] = {
                    "current": curr,
                    "previous": prev
                }

        return changed

    def _findValue(self, key: str, current = True):
        if not current and len(self.prevData) == 0:
            raise Exception("Can not find prevData")

        if key in self.commandsList:
            value = self.data if current else self.prevData

            for step in self.commands[key].split("/"):
                if step.isdigit():
                    step = int(step)
                
                value = value[step]
            
            return value
        else:
            raise Exception("Invalid key")

    def getPrevValue(self, key: str):
        self._checkValid("getPrevValue")

        return self._findValue(key, False)

    def getValue(self, key: str):
        self._checkValid("getValue")

        return self._findValue(key, True)

    def valid(self):
        return self.isValid

    def _invalid(self):
        self.isValid = False

        if self.onFail:
            self.onFail(self)

    def _loadKeys(self):
        self._checkValid("loadKeys")

        if not self.type in self.DEVICES:
            self._invalid()
            return

        import json

        self.commands = {}
        self.commandsList = []

        with open(f"Devices/{self.DEVICES[self.type]}.json", "r") as file:
            data = json.loads(file.read())

            for command in data["commands"]:
                self.commandsList.append(command)
                self.commands[command] = data[command]

            if "extends" in data and len(data["extends"]) > 0:
                for ext in data["extends"]:
                    with open(f"Devices/{ext}.json", "r") as extFile:
                        extData = json.loads(extFile.read())
                        for command in extData["commands"]:
                            self.commandsList.append(command)
                            self.commands[command] = extData[command]

    def _checkValid(self, component):
        if not self.isValid:
            raise Exception(f"error.{component}")

    def _fetchConfig(self):
        self._checkValid("fetchConfig")

        import requests

        URLs = [
            f"http://{self.ip}/settings",
            f"http://{self.ip}/rpc/Shelly.GetConfig"
        ]

        try:
            self.data["config"] = requests.get(URLs[self.gen - 1]).json()
        except:
            self._invalid()

    def _fetchStatus(self):
        self._checkValid("fetchStatus")

        import requests

        URLs = [
            f"http://{self.ip}/status",
            f"http://{self.ip}/rpc/Shelly.GetStatus"
        ]

        try:
            self.data["status"] = requests.get(URLs[self.gen - 1]).json()
        except:
            self._invalid()

    def _fetchDeviceGen(self):
        import requests

        try:
            output = requests.get(f"http://{self.ip}/shelly").json()
            if "gen" in output and output["gen"] == 2:
                self.type = output["app"]
                self.gen = 2
            else:
                self.type = output["type"]
                self.gen = 1

        except:
            self._invalid()

    def __str__(self):
        if not self.valid(): return f"Invalid object ({self.ip})"

        data = {}
        for cmd in self.commandsList:
            data[cmd] = self.getValue(cmd)

        from json import dumps
        return dumps(data)


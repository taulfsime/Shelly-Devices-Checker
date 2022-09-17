class ShellyDevice:
    DEVICES = {
        "SHSW-PM": "Shelly1PM",
        "SHUNI-1": "ShellyUNI"
    }

    def __init__(self, ip, onFail = None, onRefresh = None):
        self.ip = ip
        self.onRefresh = onRefresh
        self.onFail = onFail
        
        self._fetchDeviceGen()
        self.refresh()
        self._loadKeys()

    def refresh(self):
        self.isValid = True
        
        self._fetchStatus()
        self._fetchConfig()

        if self.onRefresh:
            self.onRefresh(self)

    def getValue(self, key: str):
        self._checkValid("getValue")

        if key in self.commandsList:
            part, path = self.commands[key].split(":")

            value = None
            if part == "status":
                value = self.status
            elif part == "config":
                value = self.config

            for step in path.split("/"):
                if step.isdigit():
                    step = int(step)
                
                value = value[step]
            
            return value
        else:
            raise Exception("Invalid key")
            

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
            self.config = requests.get(URLs[self.gen - 1]).json()
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
            self.status = requests.get(URLs[self.gen - 1]).json()
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


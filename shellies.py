class ShellyDevice:
    def __init__(self, ip):
        self.ip = ip
        
        self.refresh()
        
    def refresh(self):
        self.isValid = True
        self.gen = self._fetchDeviceGen()
        self.status = self._fetchStatus()
        self.config = self._fetchConfig()

    def valid(self):
        """
            Return true if the all the data is valid
        """

        return self.isValid

    def id(self):
        if not self.isValid:
            raise Exception("error.rssi")

        try:
            if self.gen == 1:
                return self.status["mac"]
            elif self.gen == 2:
                return self.status["sys"]["mac"]
        except:
            self.isValid = False
            return False

    def rssi(self):
        if not self.isValid:
            raise Exception("error.rssi")

        try:
            return self.status["wifi" if self.gen == 2 else "wifi_sta"]["rssi"]
        except:
            self.isValid = False
            return False


    def cc(self):
        if not self.isValid:
            raise Exception("error.cloudConnected")

        try:
            return self.status["cloud"]["connected"]
        except:
            self.isValid = False
            return False

    def _fetchConfig(self):
        if not self.isValid:
            raise Exception("error.fetchConfig")

        import requests

        URLs = [
            f"http://{self.ip}/settings",
            f"http://{self.ip}/rpc/Shelly.GetConfig"
        ]

        try:
            return requests.get(URLs[self.gen - 1]).json()
        except:
            self.isValid = False
            return False

    def _fetchStatus(self):
        if not self.isValid:
            raise Exception("error.fetchStatus")

        import requests

        URLs = [
            f"http://{self.ip}/status",
            f"http://{self.ip}/rpc/Shelly.GetStatus"
        ]

        try:
            return requests.get(URLs[self.gen - 1]).json()
        except:
            self.isValid = False
            return False

    def _fetchDeviceGen(self):
        if not self.isValid:
            raise Exception("error.fetchDeviceGen")

        import requests

        try:
            output = requests.get(f"http://{self.ip}/shelly").json()
            if "gen" in output and output["gen"] == 2:
                return 2
            else:
                return 1

        except:
            self.isValid = False
            return False
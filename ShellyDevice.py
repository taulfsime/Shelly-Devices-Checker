class ShellyDevice:
    def __init__(self, ip):
        self.ip = ip
        
        self.refresh()
        self.DEVICES = {
            "SHSW-PM": "Devices"
        }
        
    def refresh(self):
        self.isValid = True
        self._fetchDeviceGen()
        self._fetchStatus()
        self._fetchConfig()

    

    def valid(self):
        return self.isValid

    def _invalid(self):
        self.isValid = False

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
        self._checkValid("fetchGen")

        import requests

        try:
            output = requests.get(f"http://{self.ip}/shelly").json()
            if "gen" in output and output["gen"] == 2:
                self.key = output["app"]
                self.gen = 2
            else:
                self.key = output["type"]
                self.gen = 1

        except:
            self._invalid()
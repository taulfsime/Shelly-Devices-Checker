class Program():
    def __init__(self):
        from ShellyDevice import DevicesManager
        from flask import Flask

        self.config = None
        self.settings = None
        self.automations = []
        self.devicesManager = DevicesManager()

        self.apiApp = Flask("Shelly Device Checker")

    def _getDeviceInfo(self, deviceip = None, key = None):
        from Errors import UnexpectedKey, UnknownDevice
        
        try:
            print(key)
            if key is None:
                return str(self.devicesManager.getDevice(deviceip))
            
            return str(self.devicesManager.getDevice(deviceip).getValue(key))
        except UnknownDevice as e:
            return str(e)
        except UnexpectedKey as e:
            return str(e)

    def handleDevices(self):
        from ShellyDevice import DevicesManager

        def wrapper(dm: DevicesManager, atm):
            while True:
                dm.refreshAllDevices()

                for automation in atm:
                    automation.performCheck(
                        dm.getDevices(
                            automation.getTargets()
                        )
                    )

        from threading import Thread
        Thread(target=wrapper, args=(
            self.devicesManager, 
            self.automations
        )).start()

    def start(self):
        self.handleDevices()

        self.apiApp.add_url_rule("/device/<deviceip>", view_func=self._getDeviceInfo)
        self.apiApp.add_url_rule("/device/<deviceip>/<key>", view_func=self._getDeviceInfo)

        self.apiApp.run(debug=False, port=5000)

    def loadConfig(self):
        import json
        from Automations import Automation
        
        with open("config.json", "r") as file:
            self.config = json.loads(file.read())

        self.devicesManager.addDevices(self.config["devices"])
        self.automations = [Automation(x) for x in self.config["automations"]]

    def versionCheck(self):
        import json
        import requests

        with open("settings.json", "r") as file:
            self.settings = json.loads(file.read())

        if not self.settings:
            raise Exception("Can not load settings file")

        currentVersion = self.settings["version"]

        if self.settings["checkStable"]:
            try:
                stable = requests.get(self.settings["stableURL"]).json()
                if stable and "version" in stable:
                    if currentVersion != stable["version"]:
                        print("New stable version is avaliable!")
                        print("Check it here: https://github.com/taulfsime/Shelly-Devices-Checker")
            except:
                print("Error with checking for stable version")

        if self.settings["checkTest"]:
            try:
                test = requests.get(self.settings["testURL"]).json()
                if test and "version" in test:
                    if currentVersion != test["version"]:
                        print("New test version is avaliable!")
                        print("Check it here: https://github.com/taulfsime/Shelly-Devices-Checker/tree/dev")
            except:
                print("Error with checking for test version")


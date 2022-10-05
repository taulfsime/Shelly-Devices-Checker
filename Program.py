class Program:
    def __init__(self):
        from ShellyDevice import DevicesManager

        self.config = None
        self.settings = None
        self.automations = []
        self.devicesManager = DevicesManager()

    def handle(self):
        import time

        while True:
            self.devicesManager.refreshAllDevices()

            for webhook in self.webhooks:
                webhook.performCheck(
                    self.devicesManager.getDevices(
                        webhook.getTargets()
                    )
                )

            print(f"Delay of {self.config['delay']} seconds")
            time.sleep(self.config["delay"])

    def loadConfig(self):
        import json
        from Automations import Automation
        from ShellyDevice import ShellyDevice
        
        with open("config.json", "r") as file:
            self.config = json.loads(file.read())

        self.devicesManager.addDevices(self.config["devices"])
        self.webhooks = [Automation(x) for x in self.config["automations"]]

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


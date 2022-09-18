class Program:
    def __init__(self):
        self.config = None
        self.settings = None
        self.devices = []
        self.webhooks = []

    def handle(self):
        import time

        while True:
            for device in self.devices:
                device.refresh()

            for webhook in self.webhooks:
                webhook.check()

            print(f"Delay of {self.config['delay']} seconds")
            time.sleep(self.config["delay"])

    def loadConfig(self):
        import json
        from ShellyDevice import ShellyDevice
        from Webhooks import ConditionTypes
        from Webhooks import Webhook
        
        with open("config.json", "r") as file:
            self.config = json.loads(file.read())

        if "webhooks" in self.config:
            for whData in self.config["webhooks"]:
                webhook = Webhook(whData)
                self.webhooks.append(webhook)

        if "devices" in self.config:
            for deviceIP in self.config["devices"]:
                device = ShellyDevice(
                    deviceIP, 
                    onRefresh = lambda x: self.webhooksList.checkHandler(ConditionTypes.CheckVar, x),
                    onFail = lambda x: self.webhooksList.checkHandler(ConditionTypes.CanNotReach, x)
                )

                self.devices.append(device)

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


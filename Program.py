class Program:
    def __init__(self):
        self.config = None
        self.settings = None
        self.webhooks = []

    def handle(self):
        import time

        while True:
            for webhook in self.webhooks:
                webhook.performCheck()

            print(f"Delay of {self.config['delay']} seconds")
            time.sleep(self.config["delay"])

    def loadConfig(self):
        import json
        from ShellyDevice import ShellyDevice
        from Webhooks import Webhook, WebhookCondition
        
        with open("config.json", "r") as file:
            self.config = json.loads(file.read())

        for whData in self.config["webhooks"]:
            self.webhooks.append(
                Webhook(whData)
            )

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


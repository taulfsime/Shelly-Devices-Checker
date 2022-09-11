from Webhooks import ConditionTypes


class Program:
    def __init__(self):
        self.config = None
        self.settings = None
        self.webhooksList = None

    def fetchDevice(self, ip):
        from ShellyDevice import ShellyDevice
        import time
        from Webhooks import ConditionTypes
        
        for _ in range(0, self.config["attempts"]):
            try:
                device = ShellyDevice(ip)

                if device.valid():
                    deviceData = {
                        "rssi": device.rssi(),
                        "id": device.id(),
                        "cc": device.cc(),
                        "tmp": device.temperature(),
                        "ip": ip
                    }
                    
                    self.webhooksList.checkHandler(ConditionTypes.EachCheck, deviceData)
                    self.webhooksList.checkHandler(ConditionTypes.CheckVar, deviceData)
                    return True
            except:
                pass

            time.sleep(self.config["attemptDelay"])

        self.webhooksList.checkHandler(ConditionTypes.CanNotReach, { "ip": ip })
        return False

    def handle(self):
        import time

        while True:
            for device in self.config["devices"]:
                self.fetchDevice(device)
            
            print(f"Delay of {self.config['delay']} seconds")
            time.sleep(self.config["delay"])

    def loadConfig(self):
        import json
        from Webhooks import WebhooksList
        
        with open("config.json", "r") as file:
            self.config = json.loads(file.read())

        self.webhooksList = WebhooksList(self.config["webhooks"] if "webhooks" in self.config else [])

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
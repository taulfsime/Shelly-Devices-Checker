import time

def saveToCSVFile(lines):
    from datetime import datetime

    filename = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    
    lines.insert(0, ["IP", "RSSI", "ID", "CC", "TMP"])

    with open(f"outputs/{filename}.csv", "w") as file:
        for line in lines:
            file.write(", ".join([str(x) for x in line]) + "\n")

    print(f"The output was saved to {filename}")

def callDevice(attempts, attempDelay, ip):
    from shellies import ShellyDevice

    for _ in range(0, attempts):
        try:
            device = ShellyDevice(ip)

            if device.valid():
                return {
                    "rssi": device.rssi(),
                    "id": device.id(),
                    "cc": device.cc(),
                    "tmp": device.temperature()
                }
        except:
            print(f"Failed request to {ip}")

        time.sleep(attempDelay)

    return False

def main(data):
    delayTime = data["delay"]
    attempts = data["attempts"]
    attempDelay = data["attemptDelay"]
    devices = data["devices"]

    print("Started")
    
    while True:
        savedInfo = []
        for device in devices:
            output = callDevice(attempts, attempDelay, device)
            if output:
                savedInfo.append([device, output['rssi'], output['id'], output['cc'], output["tmp"]])
            else:
                savedInfo.append([device, "Failed"])
        
        saveToCSVFile(savedInfo)
        print(f"Delay of {delayTime} seconds")
        time.sleep(delayTime)

def checkVersion(settings):
    import requests

    version = settings["version"]

    if settings["checkStable"]:
        try:
            stable = requests.get(settings["stableURL"]).json()
            if stable and "version" in stable:
                if version != stable["version"]:
                    print("New stable version is avaliable!")
                    print("Check it here: https://github.com/taulfsime/Shelly-Devices-Checker")
        except:
            print("Error with checking for stable version")
    
    if settings["checkTest"]:
        try:
            test = requests.get(settings["testURL"]).json()
            if test and "version" in test:
                if version != test["version"]:
                    print("New test version is avaliable!")
                    print("Check it here: https://github.com/taulfsime/Shelly-Devices-Checker/tree/dev")
        except:
            print("Error with checking for test version")

if __name__ == "__main__":
    try:
        import os
        os.mkdir("outputs")
    except: 
        pass
    
    import json

    data = None
    settings = None

    with open("config.json", "r") as file:
        data = json.loads(file.read())
    
    with open("settings.json", "r") as file:
        settings = json.loads(file.read())

    if settings:
        checkVersion(settings)

    if data:
        main(data)
    else:
        print("Missing config file")
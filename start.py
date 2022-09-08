import requests
import json
import time

def saveToCSVFile(lines):
    from datetime import datetime

    filename = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    
    lines.insert(0, ["IP", "RSSI", "ID", "CC"])

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
                    'rssi': device.rssi(),
                    'id': device.id(),
                    'cc': device.cc()
                }
        except:
            print(f"Failed request to {ip}")

        time.sleep(attempDelay)

    return False

def main(data):
    delayTime = int(data["delay"])
    attempts = int(data["attempts"])
    attempDelay = int(data["attemptDelay"])
    devices = data["devices"]

    print("Started")
    
    while True:
        savedInfo = []
        for device in devices:
            output = callDevice(attempts, attempDelay, device)
            if output:
                savedInfo.append([device, output['rssi'], output['id'], output['cc']])
            else:
                savedInfo.append([device, "Failed"])
        
        saveToCSVFile(savedInfo)
        print(f"Delay of {delayTime} seconds")
        time.sleep(delayTime)
            
if __name__ == "__main__":
    try:
        import os
        os.mkdir("outputs")
    except: 
        pass
        
    data = None

    with open("config.json", "r") as file:
        data = json.loads(file.read())

    if data:
        main(data)
    else:
        print("Missing config file")
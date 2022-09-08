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

def getDeviceGen(ip):
    try:
        output = requests.get(f"http://{ip}/shelly").json()
        if "gen" in output and output["gen"] == 2:
            return 2
        else:
            return 1

    except:
        return False

def fetchInfo(ip, gen):
    URLs = [
        {
            "status": f"http://{ip}/status",
            "config": f"http://{ip}/settings"
        },
        {
            "status": f"http://{ip}/rpc/Shelly.GetStatus",
            "config": f"http://{ip}/rpc/Shelly.GetConfig"
        }
    ]

    try:
        status = requests.get(URLs[gen - 1]["status"]).json()
        config = requests.get(URLs[gen - 1]["config"]).json()

        return {
            "status": status,
            "config": config
        }
    except:
        return False

def callDevice(attempts, attempDelay, ip):
    for _ in range(0, attempts):
        try:
            gen = getDeviceGen(ip)
            data = fetchInfo(ip, gen)

            if gen == 1:
                rssi = data["status"]["wifi_sta"]["rssi"]
                cloudConnected = data["status"]["cloud"]["connected"]
                deviceID = data["status"]["mac"]
            elif gen == 2:
                rssi = data["status"]["wifi"]["rssi"]
                cloudConnected = data["status"]["cloud"]["connected"]
                deviceID = data["status"]["sys"]["mac"]
            
            return {
                'rssi': rssi,
                'id': deviceID,
                'cc': cloudConnected
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
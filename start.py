import requests
import json
import time

def saveToFile(lines):
    from datetime import datetime
    filename = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    
    with open(f"outputs/{filename}.txt", "w") as file:
        file.writelines(lines)
    print(f"The output was saved to {filename}")

def fetchInfo(attempts, attempDelay, ip):
    for _ in range(0, attempts):
        try:
            output = requests.get(f"http://{ip}/status").json()
            
            rssi = output["wifi_sta"]["rssi"]
            cloudConnected = output["cloud"]["connected"]
            deviceID = output["mac"]
            
            return {
                'rssi': rssi,
                'id': deviceID,
                'cc': cloudConnected
            }
            
            break
        except Exception as e:
            print(f"Failed request to {ip}")

        time.sleep(attempDelay)

    return False

def main(data):
    if data:
        delayTime = int(data["delay"])
        attempts = int(data["attempts"])
        attempDelay = int(data["attemptDelay"])
        devices = data["devices"]

        print("Started")
        
        while True:
            savedInfo = []
            for device in devices:
                output = fetchInfo(attempts=attempts, attempDelay=attempDelay, ip=device)
                if output:
                    savedInfo.append(f"IP: {device} RSSI: {output['rssi']} ID: {output['id']} CC: {output['cc']}")
                else:
                    savedInfo.append(f"IP: {device} - Failed")
            
            saveToFile(savedInfo)
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

    main(data)
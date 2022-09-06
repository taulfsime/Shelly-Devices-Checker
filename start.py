import requests
import json
from datetime import datetime
import time

data = None

with open("config.json", "r") as file:
    data = json.loads(file.read())

def saveToFile(lines):
    filename = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    
    with open(f"outputs/{filename}.txt", "w") as file:
        file.writelines(lines)
    print(f"The output was saved to {filename}")

def main():
    if data:
        delayTime = int(data["delay"])
        attempts = int(data["attempts"])
        attempDelay = int(data["attemptDelay"])
        devices = data["devices"]
        
        while True:
            savedInfo = []
            for device in devices:
                done = False
                for attempt in range(0, attempts):
                    try:
                        output = requests.get(f"http://{device}/status").json()
                        
                        rssi = output["wifi_sta"]["rssi"]
                        cloudConnected = output["cloud"]["connected"]
                        deviceID = output["mac"]
                        
                        savedInfo.append(f"IP: {device} RSSI: {rssi} ID: {deviceID} CC: {cloudConnected}")
                        
                        done = True
                        break
                    except Exception as e:
                        print(f"Failed request to {device}")
                    
                    time.sleep(attempDelay)
                if not done:
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
        
    main()
def saveToCSVFile(lines):
    from datetime import datetime

    filename = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    
    lines.insert(0, ["IP", "RSSI", "ID", "CC", "TMP"])

    with open(f"outputs/{filename}.csv", "w") as file:
        for line in lines:
            file.write(", ".join([str(x) for x in line]) + "\n")

    print(f"The output was saved to {filename}")

if __name__ == "__main__":
    try:
        import os
        os.mkdir("outputs")
    except: 
        pass

    from Program import Program
    
    app = Program()
    app.versionCheck()
    app.loadConfig()

    app.handle()
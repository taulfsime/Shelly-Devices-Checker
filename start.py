if __name__ == "__main__":
    try:
        import requests
    except ModuleNotFoundError:
        print("How to install it 'python -m pip install requests'")
        raise Exception("Missing 'requests' module")

    try:
        import datetime
    except ModuleNotFoundError:
        print("How to install it 'python -m pip install datetime'")
        raise Exception("Missing 'datetime' module")

    from Program import Program
    
    app = Program()
    app.versionCheck()
    app.loadConfig()

    app.handle()
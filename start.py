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

    try:
        import flask
    except ModuleNotFoundError:
        print("How to install it 'python -m pip install flask'")
        raise Exception("Missing 'flask' module")

    from Program import Program
    
    app = Program()
    app.versionCheck()
    app.loadConfig()

    app.start()
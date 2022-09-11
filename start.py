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
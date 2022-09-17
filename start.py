if __name__ == "__main__":
    from Program import Program
    
    app = Program()
    #app.versionCheck()
    app.loadConfig()

    app.handle()
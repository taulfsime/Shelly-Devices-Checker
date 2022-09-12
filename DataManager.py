class DataManager:
    QUERY_CreateEventLogTable = """
        CREATE TABLE IF NOT EXISTS 
        EventLog (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
            timestamp INT NOT NULL, 
            json MEDIUMTEXT NOT NULL, 
            source TEXT NOT NULL
        )
    """

    QUERY_AddToEventLog = """
        INSERT INTO EventLog
        (timestamp, json, source)
        VALUES
        (?, ?, ?)
    """

    def __init__(self):
        import sqlite3

        self.connection = sqlite3.connect("data.db")
        
        with self.connection as con:
            con.execute(self.QUERY_CreateEventLogTable)

    def addToEventLog(self, jsonData, source):
        from datetime import datetime
        ts = datetime.timestamp(datetime.now())
        
        with self.connection as con:
            con.execute(self.QUERY_AddToEventLog, (ts, jsonData, source))

    def getEventLog(self):
        with self.connection as con:
            data = con.execute("SELECT * FROM EventLog")
            for row in data:
                print(row)
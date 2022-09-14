class DataManager:
    QUERY_CreateEventLogTable = """
        CREATE TABLE IF NOT EXISTS 
        EventLog (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
            timestamp FLOAT NOT NULL, 
            json MEDIUMTEXT NOT NULL
        )
    """

    QUERY_DeleteEventLogTable = """
        DROP TABLE EventLog
    """

    QUERY_AddToEventLog = """
        INSERT INTO EventLog
        (timestamp, json)
        VALUES
        (?, ?)
    """

    def __init__(self):
        import sqlite3

        self.connection = sqlite3.connect("data.db")
        
        with self.connection as con:
            #con.execute(self.QUERY_DeleteEventLogTable)
            con.execute(self.QUERY_CreateEventLogTable)


    def addToEventLog(self, jsonData):
        from datetime import datetime
        ts = datetime.timestamp(datetime.now())
        
        with self.connection as con:
            con.execute(self.QUERY_AddToEventLog, (ts, str(jsonData)))

    def getEventLog(self):
        with self.connection as con:
            data = con.execute("SELECT * FROM EventLog")
            for row in data:
                print(row)
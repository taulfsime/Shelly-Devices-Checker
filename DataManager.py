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

    def __init__(self):
        import sqlite3

        self.connection = sqlite3.connect("data.db")
        
        with self.connection as con:
            con.execute(self.QUERY_CreateEventLogTable)
"""Module for create connection to database and
   manage this connection
"""


import sqlite3

class Database():
    """_db_file - default sqlite database file"""
    _db_file = 'wallet.db'


    def __init__(self, database_name=_db_file):

        self.database_name = database_name
        self.conn = None
        self.cursor = None


    def open_connect(self):
        """Open connection to database"""

        try:
            self.conn = sqlite3.connect(self.database_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error:
            print("Error connecting to database!")


    def close_connect(self):
        """Close connection to database"""

        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()


    def query(self,sql):
        """Execute sql expression"""

        self.cursor.execute(sql)


    def getone(self, query):
        """Get one string from database"""

        self.cursor.execute(query)
        rows = self.cursor.fetchone()
        return rows


    def get(self, table, columns, limit=None):
        """Add few strings from database"""

        query = "SELECT {0} from {1};".format(columns, table)
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows[len(rows) - limit if limit else 0:]






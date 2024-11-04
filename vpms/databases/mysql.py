import pymysql
from pymysql.cursors import DictCursor
from config import database

class mysql_database:
    def __init__(self):
        self.connection = None
        self.host = database.db_host
        self.user = database.db_user
        self.password = database.db_password
        self.database = database.db_name
        self.cursorclass = DictCursor

    def connect(self):
        if self.connection is None:
            self.connection = pymysql.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database,
                cursorclass = self.cursorclass
            )

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def cursor(self):
        if self.connection:
            return self.connection.cursor()

    def commit(self):
        if self.connection:
            self.connection.commit()

    def select_one(self, sql, params = None):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        results = cursor.fetchone()
        self.close()
        if results:
            return results
        else:
            return None

    def insert(self, sql, params = None):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        self.commit()
        self.close()

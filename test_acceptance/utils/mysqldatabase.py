import mysql.connector
from mysql.connector import errorcode


class mysqlDataBase():

    def __init__(self, host):
        self.host = host
        db = mysql.connector.connect(host=self.host)
        self.cursor = db.cursor()
    def execute_query(self,sql_query):
        self.cursor.execute(sql_query)
        return self.cursor.fetchone
    def rows(self):
        return self.cursor.rowcount


import mysql.connector
import json

class mysqlDataBase():
    def __init__(self, host, port, user, databasename):
        self.host = host
        self.port = port
        self.user = user
        self.databasename = databasename
        try:
            database = mysql.connector.connect(host=self.host, port=self.port, user=self.user, database=self.databasename)
            self.db = database
        except:
            print("connection error")
            exit(1)
    def execute_query(self, sql_query):   #result_query it is a list of elements
        try:
            cx = self.db.cursor()
            cx.execute(sql_query)
            result_query = cx.fetchall()
            print(result_query)
            return result_query
        except Exception as e:
            print("error doing query:", e)
            raise ValueError(e)


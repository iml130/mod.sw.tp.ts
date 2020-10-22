import sqlite3
import threading

sql_create_transport_orders = """CREATE TABLE "transport_orders" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"timestamp"	TEXT NOT NULL,
	"uuid"	TEXT NOT NULL,
	"agv"	TEXT NOT NULL,
	"pickup"	TEXT NOT NULL,
	"delivery"	TEXT NOT NULL,
	"refId"	TEXT NOT NULL,,
	"taskname"	TEXT NOT NULL
	"state"	INTEGER NOT NULL);"""


class TransactionLogger:
    def __init__(self):
        self.filename = "./test.db"
        self.conn = self.create_connection(self.filename)

        # create tables
        if self.conn is not None:
            # create projects table
            self.create_table(sql_create_transport_orders)

            # create tasks table
        else:
            print("Error! cannot create the database connection.")

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Exception as e:
            print(e)

        return conn

    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    my_logger = TransactionLogger()
    print("Done")

import mysql.connector
from database.database_connection import DatabaseConnection


class MySQLConnection(DatabaseConnection):
    def connect(self, db_host, db_name, db_user, db_password):
        try:
            self.conn = mysql.connector.connect(
                host=db_host,
                user=db_user,
                passwd=db_password,
                database=db_name
            )
            self.cur = self.conn.cursor()
            print('Connected to the MySQL database...')
        except Exception as error:
            print(f"Error: {error}")

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.commit()
            print('MySQL database connection closed.')

    def query(self, query):
        if self.conn and self.cur:
            self.cur.execute(query)
            result = self.cur.fetchall()
            return result
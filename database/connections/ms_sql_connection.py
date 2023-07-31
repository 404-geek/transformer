import pyodbc
from database.database_connection import DatabaseConnection


class MSSQLConnection(DatabaseConnection):
    def connect(self, db_host, db_name, db_user, db_password):
        try:
            self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+db_host+';DATABASE='+db_name+';UID='+db_user+';PWD='+ db_password)
            self.cur = self.conn.cursor()
            print('Connected to the MS SQL Server database...')
        except Exception as error:
            print(f"Error: {error}")

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.commit()
            print('MS SQL Server database connection closed.')

    def query(self, query):
        if self.conn and self.cur:
            self.cur.execute(query)
            result = self.cur.fetchall()
            return result
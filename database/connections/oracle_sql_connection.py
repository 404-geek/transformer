import cx_Oracle
from database.database_connection import DatabaseConnection


class OracleSQLConnection(DatabaseConnection):
    def connect(self, db_host, db_name, db_user, db_password):
        try:
            self.conn = cx_Oracle.connect(user=db_user, password=db_password, dsn=db_host+"/"+db_name)
            self.cur = self.conn.cursor()
            print('Connected to the Oracle SQL database...')
        except Exception as error:
            print(f"Error: {error}")

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.commit()
            print('Oracle SQL database connection closed.')

    def query(self, query):
        if self.conn and self.cur:
            self.cur.execute(query)
            result = self.cur.fetchall()
            return result
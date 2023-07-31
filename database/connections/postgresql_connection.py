import psycopg2
from database.database_connection import DatabaseConnection


class PostgreSQLConnection(DatabaseConnection):
    def connect(self, db_host, db_name, db_user, db_password):
        try:
            params = {
                "host": db_host,
                "database": db_name,
                "user": db_user,
                "password": db_password
            }
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()
            print('Connected to the PostgreSQL database...')
        except Exception as error:
            print(f"Error: {error}")

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.commit()
            print('PostgreSQL database connection closed.')

    def query(self, query):
        if self.conn and self.cur:
            self.cur.execute(query)
            result = self.cur.fetchall()
            return result

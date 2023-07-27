import psycopg2
from psycopg2 import OperationalError
from config.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


class DatabaseConnection:
    def __init__(self):
        self.conn = None
        self.cur = None

    def connect(self):
        try:
            params = {
                "host": DB_HOST,
                "database": DB_NAME,
                "user": DB_USER,
                "password": DB_PASSWORD
            }
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()
            print('Connected to the PostgreSQL database...')
            
        except (Exception, OperationalError) as error:
            print(f"Error: {error}")
            self.conn = None
            self.cur = None

    def close(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.commit()
            print('Database connection closed.')

    def query(self, query):
        if self.conn is None or self.cur is None:
            self.connect()

        self.cur.execute(query)
        result = self.cur.fetchone()
        return result

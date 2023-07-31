import pymongo
from database.database_connection import DatabaseConnection


class MongoDBConnection(DatabaseConnection):
    def connect(self, db_host, db_name):
        try:
            self.conn = pymongo.MongoClient(db_host)
            self.cur = self.conn[db_name]
            print('Connected to the MongoDB database...')
        except Exception as error:
            print(f"Error: {error}")

    def close(self):
        if self.conn:
            self.conn.close()
            print('MongoDB database connection closed.')

    def query(self, collection_name, query_filter=None):
        if query_filter is None:
            query_filter = {}
        if self.conn and self.cur:
            collection = self.cur[collection_name]
            result = collection.find(query_filter)
            return list(result)
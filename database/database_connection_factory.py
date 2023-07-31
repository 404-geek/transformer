from database.database_connection import DatabaseConnection
from database.connections.mysql_connection import MySQLConnection
from database.connections.oracle_sql_connection import OracleSQLConnection
from database.connections.ms_sql_connection import MSSQLConnection
from typing import Type


DatabaseConnectionType = Type[DatabaseConnection]


class DatabaseConnectionFactory:

    _database_connections = {}

    # register a database connection
    @staticmethod
    def register_database_connection(key:str, database_connection: DatabaseConnectionType) -> None:
        ''' Registering a database connection using db type'''

        DatabaseConnectionFactory._database_connections[key] = database_connection


    # get database connection based on feed type
    @staticmethod
    def get_database_connection(db_type:str) -> DatabaseConnection :
        ''' Get required database connection based on db type '''

        database_connection = DatabaseConnectionFactory._database_connections.get(db_type)
        if database_connection:
            return database_connection()
        else:
            raise ValueError(f"Unsupported feed type: {db_type}")
        


# Registering database connections
DatabaseConnectionFactory.register_database_connection("MySQL", MySQLConnection)
DatabaseConnectionFactory.register_database_connection("OracleSQL", OracleSQLConnection)
DatabaseConnectionFactory.register_database_connection("MSSQL", MSSQLConnection)
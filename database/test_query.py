from database.connection import DatabaseConnection


def test_query():
    db = DatabaseConnection()
    db.connect()
    
    if db.conn is not None:
        print('PostgreSQL database version:')
        result = db.query('SELECT version()')
        print(result)

        db.close()

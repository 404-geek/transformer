from database.database_connection_factory import DatabaseConnectionFactory


def test_postgresql_query():
    db = DatabaseConnectionFactory.get_database_connection("PostgreSQL")
    db.connect("localhost", "testdb", "postgres", "postgres")
    result = db.query("SELECT * FROM users")
    print(result)
    db.close()


def test_mysql_query():
    db = DatabaseConnectionFactory.get_database_connection("MySQL")
    db.connect('localhost', 'mydatabase', 'myuser', 'mypassword')
    result = db.query("SELECT * FROM test_table")
    print(result)
    db.close()


def test_mongodb_query():
    db = DatabaseConnectionFactory.get_database_connection("MongoDB")
    db.connect('localhost', 'mydatabase')
    result = db.query('mycollection', {"field": "value"}) 
    print(result)
    db.close()

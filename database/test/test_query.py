from database.database_connection_factory import DatabaseConnectionFactory


def test_mysql_query():
    db = DatabaseConnectionFactory.get_database_connection("MySQL")
    db.connect('localhost', 'mysql', 'stride', '123456')
    result = db.query("SELECT * FROM db")
    print(result)
    db.close()


def test_oracle_sql_query():
    db = DatabaseConnectionFactory.get_database_connection("OracleSQL")
    db.connect('localhost', 'mydatabase', 'myuser', 'mypassword')
    result = db.query("SELECT * FROM db")
    print(result)
    db.close()


def test_ms_sql_query():
    db = DatabaseConnectionFactory.get_database_connection("MSSQL")
    db.connect('localhost', 'mydatabase', 'myuser', 'mypassword')
    result = db.query("SELECT * FROM db")
    print(result)
    db.close()


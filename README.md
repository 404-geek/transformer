# transformer service


## Steps to Setups Server ##

- INSTALL python 3.7.

```
sudo apt update
sudo apt install python3.7
sudo apt install python3-pip
```

- Create or Update the credential and other required things .env file in config.


- Create a Virtual Environment outside Project folder

```
virtualenv -p python3 venv
```

- Activate the Virtual Environment.

```
 > source venv/bin/activate (Linux)
 > venv\Scripts\Activate (Windows)
```

- Install required python library.

```
pip install -r requirements.txt
```



## Env Structure

```
# Kafka Configuration

KAFKA_SERVER=
TRANSFORMER_CHANNEL=
AGGREGATOR_CHANNEL=
DYNAMODB_KEY=
API_URI=
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=
```


# Transformers Boilerplate

## Create Transformer

- Create a transformer by inheriting from ```BaseTransformer``` class
- Specify the transformations logic in ```add_transformations``` method as mentioned below
- ```kwargs``` handles any keyword arguments like ```source_file_type```, ```destination_file_type```,  ```start```, ```end```, ```last```, etc

```py
# sample_transformer.py


from utils.transformer.base_transformer import BaseTransformer


class SampleTransformer(BaseTransformer):
    
    # add specified transformations to the given chunk
    def add_transformations(self, data: object, **kwargs) -> str:
        ''' Add required transformations here '''
```
<br/>

### Register Transformer


- Register your transformer in the ```TransformerFactory``` using ```register_transformer``` method which takes a string and the transformer as arguments.

```py
# transformer_factory.py


# Registering transformers
TransformerFactory.register_transformer("PRODUCT", ProductTransformer)
TransformerFactory.register_transformer("STORE", StoreTransformer)
TransformerFactory.register_transformer("AMG_TO_SFCC_LOCATION", AMGtoSFCCLocationTransformer)
TransformerFactory.register_transformer("SAMPLE", SampleTransformer)

```

<br/>


## Example Transformer
### Sample Transformer

```py
# sample_transformer.py


from utils.transformer.base_transformer import BaseTransformer


class SampleTransformer(BaseTransformer):
    
    # add specified transformations to the given chunk
    def add_transformations(self, data: object, **kwargs) -> str:
        ''' Add required transformations here '''

```

Register the transformer in the ```TransformerFactory``` using ```register_transformer``` method

```py
# transformer_factory.py


from transformers.product_transformer import ProductTransformer
from transformers.store_transformer import StoreTransformer
from transformers.amg_to_sfcc_location_transformer import AMGtoSFCCLocationTransformer
from transformers.sample_transformer import SampleTransformer
from utils.transformer.base_transformer import BaseTransformer
from typing import Type


TransformerType = Type[BaseTransformer]

class TransformerFactory:

    _transformers = {}

    # register a transformer
    @staticmethod
    def register_transformer(key:str, transformer: TransformerType) -> None:
        ''' Registering a transformer using feed type'''

        TransformerFactory._transformers[key] = transformer


    # get transformer based on feed type
    @staticmethod
    def get_transformer(feed_type:str) -> BaseTransformer :
        ''' Get required transformer based on feed type '''

        transformer = TransformerFactory._transformers.get(feed_type)
        if transformer:
            return transformer()
        else:
            raise ValueError(f"Unsupported feed type: {feed_type}")



# Registering transformers
TransformerFactory.register_transformer("PRODUCT", ProductTransformer)
TransformerFactory.register_transformer("STORE", StoreTransformer)
TransformerFactory.register_transformer("AMG_TO_SFCC_LOCATION", AMGtoSFCCLocationTransformer)
TransformerFactory.register_transformer("SAMPLE", SampleTransformer)

```


## Test Transformers

- To test transformers you can [refer this](./test)

<br/>

# API Boilerplate

## Overview

- RequestHandler is available to perform api calls.
- It takes 4 arguments - `url`, `method`, `headers`, `data`, `params`, `json`, and `files`
- `url` and `method` are required arguments and remaining arguments are optional.

```py

def RequestHandler(url, method, headers=None, data=None, params=None, json=None, files=None):
    try:
        response = requests.request(
            method,
            url,
            headers,
            data,
            params,
            json,
            files
        )
        return response
    except Exception as e:
        print("Error: %s" % e)

```


## Usage

- Use `RequestHandler` method by passing `url`, `method`, `headers` and `data`.
- It returns a `response` object.
- Here is a `test_api.py` implementing `RequestHandler`

```py
import json
from config.config import API_URI
from api.api import RequestHandler


def test_api():
    url = f"{API_URI}/test"
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"mode": "test"})
    response = RequestHandler(url=url, method='post', headers=headers, data=data)
    if response != None:
        print(f"Response: {response.text}")

```

<br/>

# Database Boilerplate

## Overview

- Using Factory design pattern to fetch the db connection base on `db_type`.
- `register_database_connection` registers the db connection with a `db_type` key.
- `get_database_connection` returns a db connection based on `db_type`.


```py
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

```

## MySQL connection

- Uses `mysql.connector` driver to perform operations on `MySQL` database.
- Extends `DatabaseConnection` class to create the database connection for MySQL.

```py
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

```

## Oracle SQL connection

- Uses `cx_Oracle` driver to perform operations on `Oracle SQL` database.
- Extends `DatabaseConnection` class to create the database connection for Oracle SQL.

```py
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

```

## MS SQL connection

- Uses `pyodbc` driver to perform operations on `MS SQL` database.
- Extends `DatabaseConnection` class to create the database connection for MS SQL.

```py
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
```



## Usage

- Establish the db connection by creating a `DatabaseConnectionFactory` object and then calling `get_database_connection` method py passing `db_type`.
- Here is a `test_query.py` file which performs a query on all these database connections.

```py
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

```
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
- It takes 4 arguments - `url`, `method`, `headers`, and `data`
- `method` is of type `HttpMethod` which is a enum for `get`, `post`, `put` and `delete` http methods as shown below.

```py

class HttpMethod(Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"


def RequestHandler(url: str, method: HttpMethod, headers: object, data: json):
    try:
        if method == HttpMethod.GET:
            response = requests.get(url, headers=headers)
        elif method == HttpMethod.POST:
            response = requests.post(url, headers=headers, data=data)
        elif method == HttpMethod.PUT:
            response = requests.put(url, headers=headers, data=data)
        elif method == HttpMethod.DELETE:
            response = requests.delete(url, headers=headers)
        else:
            print(f"Invalid method {method} specified.")
            return None
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
from api.api import RequestHandler, HttpMethod


def test_api():
    url = f"{API_URI}/test"
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"mode": "test"})
    response = RequestHandler(url=url, method=HttpMethod.POST, headers=headers, data=data)
    if response != None:
        print(f"Response: {response.text}")

```

<br/>

# Database Boilerplate

## Overview

- Using `psycopg2` driver to perform operations on `PostgreSQL` database.
- Implementing a `DatabaseConnection` class and `connect` method to connect to the db with specified credentials.
- `close` method will disconnect the connection with the db.
- `query` method takes one argument called query and performs the query operations.

```py
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


```

## Usage

- Establish the db connection by creating a `DatabaseConnection` object and then calling `connect` method.
- Here is a `test_query` which performs a query to print the db version using `query` method.

```py
from database.connection import DatabaseConnection


def test_query():
    db = DatabaseConnection()
    db.connect()
    
    if db.conn is not None:
        print('PostgreSQL database version:')
        result = db.query('SELECT version()')
        print(result)

        db.close()

```
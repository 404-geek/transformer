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
```


# Transformers Boilerplate

## Create Transformer

- Create a transformer by inheriting from ```BaseTransformer``` class
- Specify the transformations logic in ```add_transformations``` method as metioned below

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
TransformerFactory.register_transformer("CSV", CsvTransformer)
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
from transformers.csv_transformer import CsvTransformer
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
TransformerFactory.register_transformer("CSV", CsvTransformer)
TransformerFactory.register_transformer("AMG_TO_SFCC_LOCATION", AMGtoSFCCLocationTransformer)
TransformerFactory.register_transformer("SAMPLE", SampleTransformer)

```


## Test Transformers

- To test transformers you can [refer this](https://github.com/404-geek/transformer/tree/main/test)
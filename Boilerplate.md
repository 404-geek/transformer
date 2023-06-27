# Transformers Boilerplate

## Create Transformer

- Create a transformer by inheriting from ```BaseTransformer``` class
- Specify the transformations logic in ```add_transformations``` method as metioned below

```py
# test_transformer.py


from utils.transformer.base_transformer import BaseTransformer


class TestTransformer(BaseTransformer):
    
    # add specified transformations to the given chunk
    def add_transformations(self, data: object) -> object:
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
TransformerFactory.register_transformer("TEST", TestTransformer)

```

<br/>

## Example Transformer
### Test Transformer

```py
# test_transformer.py


from utils.transformer.base_transformer import BaseTransformer


class TestTransformer(BaseTransformer):
    
    # add specified transformations to the given chunk
    def add_transformations(self, data: object) -> object:
        ''' Add required transformations here '''

```

Register the transformer in the ```TransformerFactory``` using ```register_transformer``` method

```py
# transformer_factory.py


from transformers.product_transformer import ProductTransformer
from transformers.csv_transformer import CsvTransformer
from test.test_transformer import TestTransformer
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
TransformerFactory.register_transformer("TEST", TestTransformer)

```
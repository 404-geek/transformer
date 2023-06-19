# Transformers Boilerplate

## Create Transformer

- Create a transformer by inheriting from ```BaseTransformer``` class
- Add all the logic required in ```transform``` method which includes getting the chunk data, validating it and calling the transformations method
- Specify the transformations logic in ```add_transformations``` method as metioned below

```py
# test_transformer.py


from utils.base_tranformer import BaseTransformer

class TestTransformer(BaseTransformer):
    
    # Transform method which transforms the given chunk by following the given steps
    def transform(self, bucket_name: str, file_name: str, file_type: str, uuid: str, index: int, start: int, end: int, directory: str, **kwargs) -> None:
        '''
            Tranform the given chunk by following the given steps
            
            - Fetch data from s3 bucket using get_data method which takes 
              s3_bucket, source, chunk_start, and chunk_end as arguments
            - Validate the given chunk data if it is not validated
            - Add specified transformations for the transformer in add_transformations method
            - Remove extra tags or code that you added to validate the file before generating a batch file
            - Generate a batch file for the given chunk using generate_batch method which takes
              directory, data, file_type, chunk_start, and chunk_end as arguments

        '''

    # add specified transformations to the given chunk
    def add_transformations(self, data):
        ''' Add required transformations here '''
```
<br/>

### Transform Method

1. Fetch the data from s3 bucket using ```get_data``` method which takes bucket_name, file_name, start, and end as arguments

```py
def transform(self, bucket_name: str, file_name: str, file_type: str, uuid: str, index: int, start: int, end: int, directory: str, **kwargs) -> None:

    ''' get data from s3 bucket '''
    data = self.get_data(bucket_name, file_name, start, end)

    # ...

```

2. Validate the file (for example:- xml file) before making the required transformations to the given chunk. For 'xml' file you can use ```generate_valid_xml_file``` method which is already present in the ```BaseTransformer```

3. Create a ```add_transformations``` method inside your transformer (example:- ```TestTransformer```) and place all your specified transformation logic in this method. Make sure your chunk is validated before transforming the chunk data.

```py
def transform(self, bucket_name: str, file_name: str, file_type: str, uuid: str, index: int, start: int, end: int, directory: str, **kwargs) -> None:

    # ...

    ''' add transformations to the chunk accordingly '''
    data = self.add_transformations(data)

    # ...

```

4. Remove all the extra tags or data added to validate the chunk data. Make sure you remove everything and make it as the originla chunk before creating a batch file.

5. Generate a batch file for the given chunk data using ```generate_batch``` method. It takes uuid, index, lines, file_type, and start as arguments.

```py
def transform(self, bucket_name: str, file_name: str, file_type: str, uuid: str, index: int, start: int, end: int, directory: str, **kwargs) -> None:

    # ...

    ''' generate batch file for the given chunk after transformations '''
    self.generate_batch(directory, uuid, index, lines, file_type, start)

    # ...

```

6. Register your transformer in the ```TransformerFactory``` using ```register_transformer``` method which takes a string and the transformer as arguments.

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


from utils.tranformer.base_transformer import BaseTransformer


class TestTransformer(BaseTransformer):
    
    # Transform method which transforms the given chunk by following the given steps
    def transform(self, bucket_name: str, file_name: str, file_type: str, uuid: str, index: int, start: int, end: int, directory: str, **kwargs) -> None:
        '''
            Tranform the given chunk by following the given steps
            
            - Fetch data from s3 bucket using get_data method which takes 
              bucket_name, file_name, start, and end as arguments
            - Validate the given chunk data if it is not validated
            - Add specified transformations for the transformer in add_transformations method
            - Remove extra tags or code that you added to validate the file before generating a batch file
            - Generate a batch file for the given chunk using generate_batch method which takes
              directory, data, file_type, start, and end as arguments

        '''
        

        ''' get data from s3 bucket '''
        data = self.get_data(bucket_name, file_name, start, end)


        ''' validate the data chunk if required '''


        ''' add transformations to the chunk accordingly '''
        data = self.add_transformations(data)


        ''' remove any additional added tags while validating the chunk '''
        

        ''' generate batch file for the given chunk after transformations '''
        self.generate_batch(directory, uuid, index, data, file_type, start)


    # add specified transformations to the given chunk
    def add_transformations(self, data):
        ''' Add required transformations here '''

```

Register the transformer in the ```TransformerFactory``` using ```register_transformer``` method

```py
# transformer_factory.py


from transformers.product_transformer import ProductTransformer
from transformers.csv_transformer import CsvTransformer
from test.test_transformer import TestTransformer
from utils.base_transformer import BaseTransformer
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
# Transformers Boilerplate

## Create Transformer

- Create a transformer by inheriting from ```BaseTransformer``` class
- Add all the logic required in ```transform``` method which includes getting the chunk data, validating it and calling the transformations method
- Specify the transformations logic in ```add_transformations``` method as metioned below

```py
# test_transformer.py


from utils.base_tranformer import BaseTransformer

class TestTransformer(BaseTransformer):
    
    def transform(self, *args, **kwargs):
        ''' Transform the chunk here '''

    def add_transformations(self, *args, **kwargs):
        ''' Add required transformaton shere '''
```
<br/>

### Transform Method

1. Get all the required arguments from the arguments(*args) or  keyword arguments(**kwargs)

```py
def transform(self, *args, **kwargs):

    ''' get arguments '''
    source = kwargs['source']
    file_type = kwargs['file_type']
    chunk_start = kwargs['chunk_start']
    chunk_end = kwargs['chunk_end']
    s3_bucket = kwargs['s3_bucket']
    directory = kwargs['directory']

    # ...

```

2. Fetch the data from s3 bucket using ```get_data``` method which takes s3_bucket, source, chunk_start and chunk_end as arguments

```py
def transform(self, *args, **kwargs):

    # ...

    ''' get data from s3 bucket '''
    data = self.get_data(s3_bucket, source, chunk_start, chunk_end)

    # ...

```

3. Validate the file (for example:- xml file) before making the required transformations to the given chunk. For 'xml' file you can use ```generate_valid_file``` method which is already present in the ```BaseTransformer```

4. Create a ```add_transformations``` method inside your transformer (example:- ```TestTransformer```) and place all your specified transformation logic in this method. Make sure your chunk is validated before transforming the chunk data.

```py
def transform(self, *args, **kwargs):

    # ...

    ''' add transformations to the chunk accordingly '''
    data = self.add_transformations(data)

    # ...

```

5. Remove all the extra tags or data added to validate the chunk data. Make sure you remove everything and make it as the originla chunk before creating a batch file.

6. Generate a batch file for the given chunk data using ```generate_batch``` method. It takes directory, data, file_type, chunk_start and chunk_end as arguments.

```py
def transform(self, *args, **kwargs):

    # ...

    ''' generate batch file for the given chunk after transformations '''
    self.generate_batch(directory, data, file_type, chunk_start, chunk_end)

    # ...

```

7. Register your transformer in the ```TransformerFactory``` using ```register_transformer``` method which takes a string and the transformer as arguments.

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


from utils.base_tranformer import BaseTransformer


class TestTransformer(BaseTransformer):
    
    def transform(self, *args, **kwargs):

        ''' get arguments '''
        source = kwargs['source']
        file_type = kwargs['file_type']
        chunk_start = kwargs['chunk_start']
        chunk_end = kwargs['chunk_end']
        s3_bucket = kwargs['s3_bucket']
        directory = kwargs['directory']

        ''' get data from s3 bucket '''
        data = self.get_data(s3_bucket, source, chunk_start, chunk_end)


        ''' validate the data chunk if required '''


        ''' add transformations to the chunk accordingly '''
        data = self.add_transformations(data)


        ''' remove any additional added tags while validating the chunk '''
        

        ''' generate batch file for the given chunk after transformations '''
        self.generate_batch(directory, data, file_type, chunk_start, chunk_end)

    
    def add_transformations(self, *args, **kwargs):
        ''' Add required transformations here '''

```

Register the transformer in the ```TransformerFactory``` using ```register_transformer``` method

```py
# transformer_factory.py


from transformers.product_transformer import ProductTransformer
from transformers.csv_transformer import CsvTransformer
from test.test_transformer import TestTransformer


class TransformerFactory:

    _transformers = {}

    @staticmethod
    def register_transformer(key, transformer):
        TransformerFactory._transformers[key] = transformer

    @staticmethod
    def get_transformer(feed_type):
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
# Test Transformers


## Test Transformer Boilerplate

1. **Initialization**: Create an instance of the required transformer from **TransformerFactory** by passing ```feed_type```.

```py
transformer = TransformerFactory.get_transformer(feed_type)
```

2. **Get Transformed Chunk**: **get_transformed_chunk** method is used to get the transformed chunk after adding the required transformations. 
- It takes ```data```, ```source_file_type```, ```destination_file_type```, ```start```, ```last``` as input. 
- You can also pass other arguments such as ```file_name```, ```uuid```, ```index```, ```end```, etc that are handled by ```kwargs```.

```py
transformed_data = transformer.get_transformed_chunk(data=data, start=start, last=last, source_file_type=source_file_type, destination_file_type=destination_file_type, **kwargs)
```

<br/>

## Testing individual transformers


### How to run tests

- Run the below command in the terminal to test required transformers
- Provide the input file path by using ```source_file_path``` in cmd
- For reference you can use the files available in ```test_input_files``` folder
- After adding transformations the output is generated in the specified destination path by ```destination_file_path``` in cmd
- Below are the command line arguments for testing the transformers 

```
required arguments:
  --feed_type                   FEED_TYPE                   Set the feed type (str)  
  --source_file_path            SOURCE_FILE_PATH            Set the path of the input file (str)
  --source_file_type            SOURCE_FILE_TYPE            Set input file type (str)
  --destination_file_path       DESTINATION_FILE_PATH       Set the path of the output file (str)
  --destination_file_type       DESTINATION_FILE_TYPE       Set output file type (str)

optional arguments:
  --start                       START                       Set start of the chunk data (int)       
  --end                         END                         Set end of the chunk data (int)
  --last                        LAST                        Set if current chunk data is last (bool) 
  --split_points                SPLIT_POINTS                Set split points of the file (int[])

custom arguments:
  You can also pass custom arguments. It should start with '--' and should have a '=' and then the value. There should not be any spaces between the words ('--event_name' is accepted, '--event name' is not accepted)

  Example: --event_name=test
```

### Example 

- Testing StoreTransformer

```py
# test store transformer with start and last
python3 test/test_transformers.py --feed_type=STORE --start=0 --last=True --source_file_path=test/input/test_store.csv --source_file_type=csv --destination_file_path=test/output --destination_file_type=csv 

# test store transformer with start and end
python3 test/test_transformers.py --feed_type=STORE --start=0 --end=5013 --source_file_path=test/input/test_store.csv --source_file_type=csv --destination_file_path=test/output --destination_file_type=csv 

# test store transformer with split points
python3 test/test_transformers.py --feed_type=STORE --split_points=2022,5013,8548,13252,15046,20000 --source_file_path=test/input/test_store.csv --source_file_type=csv --destination_file_path=test/output --destination_file_type=csv
```

- Testing ProductTransformer

```py
# test product transformer with start and last
python3 test/test_transformers.py --feed_type=PRODUCT --start=0 --last=True --source_file_path=test/input/test_product.xml --source_file_type=xml --destination_file_path=test/output --destination_file_type=xml 

# test product transformer with start and end
python3 test/test_transformers.py --feed_type=PRODUCT --start=0 --end=1902 --source_file_path=test/input/test_product.xml --source_file_type=xml --destination_file_path=test/output --destination_file_type=xml 

# test product transformer with split points
python3 test/test_transformers.py --feed_type=PRODUCT --split_points=2790,4550,6017,9000,14000,21037,25142,30543,42009,50000 --source_file_path=test/input/test_product.xml --source_file_type=xml --destination_file_path=test/output --destination_file_type=xml
```

- Testing AMGtoSFCCLocationTransformer

```py
# test amg to sfcc location transformer with start and last
python3 test/test_transformers.py --feed_type=AMG_TO_SFCC_LOCATION --start=0 --last=True --source_file_path=test/input/test_amg_sfcc.csv --source_file_type=csv --destination_file_path=test/output --destination_file_type=xml

# test amg to sfcc location transformer with start and end
python3 test/test_transformers.py --feed_type=AMG_TO_SFCC_LOCATION --start=0 --end=1502 --source_file_path=test/input/test_amg_sfcc.csv --source_file_type=csv --destination_file_path=test/output --destination_file_type=xml

# test amg to sfcc location transformer with split points
python3 test/test_transformers.py --feed_type=AMG_TO_SFCC_LOCATION --split_points=536,1043,1604,2012,2624,3000 --source_file_path=test/input/test_amg_sfcc.csv --source_file_type=csv --destination_file_path=test/output --destination_file_type=xml
```

## Unit testing

### Overview

A set of assert methods provided by unittest.TestCase allows you to check for conditions such as:

- ```assertEqual(a, b)```: Check a and b are equal
- ```assertIsNone(x)```: Check that x is None
- ```assertIsNotNone(x)```: Check that x is not None
- ```assertRaises(exception, callable, *args, **kwargs)```: Check that an exception is raised when calling a function.

### Test Sections

#### **TestTransformerFactory**

- This section tests the ```TransformerFactory``` class to ensure it correctly returns the right kind of transformer based on the input argument. 
- It also checks for the exception handling, in case of invalid arguments or absence of arguments.

```py
class TestTransformerFactory(unittest.TestCase):
    def setUp(self):
        self.transformer_factory = TransformerFactory()

    def test_invalid_transformers(self):
        with self.assertRaises(ValueError):
            self.transformer_factory.get_transformer('INVALID')
        with self.assertRaises(TypeError):
            self.transformer_factory.get_transformer()

```

#### **TestStoreTransformer**
- This part is designed to test the ```STORE``` type transformer. 
- It verifies the transformation of input CSV data into a predefined format and ensures error handling for invalid CSV input.
- The tests cover a variety of cases, including valid CSV data, CSV data starting at a non-zero index, and invalid data such as nonexistent files or None values.

```py
class TestStoreTransformer(unittest.TestCase):
    def setUp(self):
        self.transformer = TransformerFactory().get_transformer('STORE')

    def test_add_transformations_with_valid_data(self):
        data = StringIO("STORE,QTY,VAL,BARCODE,DATE\n1,2,3,1234,20230303")
        transformed_data = self.transformer.add_transformations(data, start=0, last=True)
        expected_output = 'Units,Sold at Price,UPC Number,Transaction Line,Transaction Date,Location Code,Is Price Override,Is Markup\n2,3,1234,1,2023-03-03 00:00:00,00001,0,0\n'
        self.assertEqual(transformed_data, expected_output)
    # ... remaining tests mentioned in the file

```


#### **TestProductTransformer**

- This section tests the ```PRODUCT``` type transformer, checking if it can successfully transform XML data by adding additional tags (such as datetime, color, and order-fulfill). 
- It also tests for error handling in cases where the XML data is invalid or None.

```py
class TestProductTransformer(unittest.TestCase):
    def setUp(self):
        self.transformer = TransformerFactory().get_transformer('PRODUCT')

    def test_add_transformations_with_valid_xml(self):
        xml_data = "<products><product><upc>123</upc><step-quantity>1</step-quantity></product></products>"
        root = ET.fromstring(xml_data)
        transformed_data = self.transformer.add_transformations(root, start=0, last=True)
        root = ET.fromstring(transformed_data)
        self.assertIsNotNone(root.find('.//datetime'))
        self.assertIsNotNone(root.find('.//color'))
        self.assertIsNotNone(root.find('.//order-fulfill'))
    # ... remaining tests mentioned in the file

```

#### **TestAMGtoSFCCLocationTransformer**

- This part tests the ```AMG_TO_SFCC_LOCATION``` type transformer. 
- It verifies the transformation of store IDs into a predefined format and checks if CSV data is transformed into the correct XML format. 
- Error handling for invalid data, including non-numeric store IDs and invalid CSV data, is also tested here.

```py
class TestAMGtoSFCCLocationTransformer(unittest.TestCase):
    def setUp(self):
        self.transformer = TransformerFactory().get_transformer('AMG_TO_SFCC_LOCATION')

    def test_transform_store_id_with_valid_data(self):
        self.assertEqual(self.transformer.transform_store_id('00001'), 'DC01')
        self.assertEqual(self.transformer.transform_store_id('00010'), 'DC10')
        self.assertEqual(self.transformer.transform_store_id('00960'), '960')
        self.assertEqual(self.transformer.transform_store_id(960), '960')
        self.assertEqual(self.transformer.transform_store_id(1), 'DC01')
        self.assertEqual(self.transformer.transform_store_id(10), 'DC10')
    # ... remaining tests mentioned in the file

```




### Usage

- To perform unit tests for all transformers

```py
# to perform unit tests
python3 test/test_all_transformers.py
```


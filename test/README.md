# Test Transformers


## Store Transformer
### Usage

1. **Initialization**: Create an instance of the **StoreTransformer** from **TransformerFactory**.

```py
transformer = TransformerFactory.get_transformer("STORE")
```

2. **Adding Transformations**: Utilize the **add_transformations** method to perform transformations on the data. Pass in the data (as a **DataFrame**), and any optional parameters like **start**.

```py
transformed_data = transformer.add_transformations(data, start=0, **kwargs)
```

The transformed data will contain the following columns:

- Transaction Line
- Transaction Date
- Location Code
- Is Price Override
- Is Markup
- Units
- Sold at Price
- UPC Number

<br/>

## Product Transformer
### Usage

1. **Initialization**: Create an instance of the **ProductTransformer** from **TransformerFactory**.

```py
transformer = TransformerFactory.get_transformer("PRODUCT")
```

2. **Adding Transformations**: Utilize the **add_transformations method** to perform transformations on the data. Pass in the XML data (as an **ElementTree** Element), and any optional parameters.

```py
transformed_data = transformer.add_transformations(xml_data, **kwargs)
```

The transformed data will have additional elements appended to each **product** element:

- **datetime**: The current timestamp.
- **color**: Set to 'brown' if the product has a UPC, otherwise set to 'black'.
- **order-fulfill**: If **step-quantity** is '1', this element is appended with value 'ordered'.

<br/>

## AMG to SFCC Location Transformer
### Usage

1. **Initialization**: Create an instance of the **AMGtoSFCCLocationTransformer** from **TransformerFactory**.

```py
transformer = TransformerFactory.get_transformer("AMG_TO_SFCC_LOCATION")
```

2. **Adding Transformations**: Use the **add_transformations** method to transform the data. Pass in the data (as a **DataFrame**), and any optional arguments like **start** and **last**.

```py
transformed_data = transformer.add_transformations(data, start=0, last=True, **kwargs)
```

**Store ID Transformation**: The **transform_store_id** method is used internally to transform store IDs. It's not intended for external use, but can be called separately if needed.

```py
transformed_store_id = transformer.transform_store_id(store_id)
```

<br/>

## Testing individual transformers

### Note

- Provide input file inside ```input``` folder before running the tests
- Input folder should only contain one file to perform test
- For reference you can copy paste the files available in ```test_input_files``` folder

### How to run tests

- Run the below command in the terminal to test required transformers
- It generates the output in the ```output``` folder with name ```{filename}_batch.txt```
- Below are the command line arguments for testing the transformers 

```
required arguments:
  --feed_type                   FEED_TYPE                   Set the feed type (str)                       
  --destination_file_type       DESTINATION_FILE_TYPE       Set destination file type (str)

optional arguments:
  --start                       START                       Set start of the chunk data (int)       
  --end                         END                         Set end of the chunk data (int)
  --last                        LAST                        Set if current chunk data is last (bool) 
  --split_points                SPLIT_POINTS                Set split points of the file (int[])

custom arguments:
  You can also pass custom arguments. It should start with '--' and should have a '=' and then the value. There should not be any spaces between the words ('--file_name' is accepted, '--file name' is not accepted)

  Example: --file_name=test
```

### Example 

- Testing StoreTransformer

```py
# test store transformer with start and last
python3 test/test_transformers.py --feed_type=STORE --start=0 --last=True --destination_file_type=csv 

# test store transformer with start and end
python3 test/test_transformers.py --feed_type=STORE --start=0 --end=5013 --destination_file_type=csv 

# test store transformer with split points
python3 test/test_transformers.py --feed_type=STORE --split_points=2022,5013,8548,13252,15046,20000 --destination_file_type=csv
```

- Testing ProductTransformer

```py
# test product transformer with start and last
python3 test/test_transformers.py --feed_type=PRODUCT --start=0 --last=True --destination_file_type=xml 

# test product transformer with start and end
python3 test/test_transformers.py --feed_type=PRODUCT --start=0 --end=1902 --destination_file_type=xml 

# test product transformer with split points
python3 test/test_transformers.py --feed_type=PRODUCT --split_points=2790,4550,6017,9000,14000,21037,25142,30543,42009,50000 --destination_file_type=xml
```

- Testing AMGtoSFCCLocationTransformer

```py
# test amg to sfcc location transformer with start and last
python3 test/test_transformers.py --feed_type=AMG_TO_SFCC_LOCATION --start=0 --last=True --destination_file_type=xml

# test amg to sfcc location transformer with start and end
python3 test/test_transformers.py --feed_type=AMG_TO_SFCC_LOCATION --start=0 --end=1502 --destination_file_type=xml

# test amg to sfcc location transformer with split points
python3 test/test_transformers.py --feed_type=AMG_TO_SFCC_LOCATION --split_points=536,1043,1604,2012,2624,3000 --destination_file_type=xml
```

## Unit testing

- To perform unit tests for all transformers

```py
# to perform unit tests
python3 test/test_all_transformers.py
```

## Error Handling
- Errors like invalid input data or issues during transformation are handled by printing an error message and raising the exception.

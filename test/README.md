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

- To perform unit tests for all transformers

```py
# to perform unit tests
python3 test/test_all_transformers.py
```

## Error Handling
- Errors like invalid input data or issues during transformation are handled by printing an error message and raising the exception.

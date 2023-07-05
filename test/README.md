## Test Transformers


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
  --start                       START                       Set start of the chunk data (int)                
  --last                        LAST                        Set if current chunk data is last (bool)                
  --destination_file_type       DESTINATION_FILE_TYPE       Set destination file type (str)
```

```py
# for testing store transformer
python3 test/test_transformers.py --feed_type=STORE --start=0 --last=True --destination_file_type=csv 

# for testing product transformer
python3 test/test_transformers.py --feed_type=PRODUCT --start=0 --last=True --destination_file_type=xml 

# for testing amg to sfcc location transformer
python3 test/test_transformers.py --feed_type=AMG_TO_SFCC_LOCATION --start=0 --last=True --destination_file_type=xml
```

- To perform unit tests for all transformers

```py
# to perform unit tests
python3 test/test_all_transformers.py
```

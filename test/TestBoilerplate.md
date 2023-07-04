### Test Transformers

- Run the below command in the terminal to test required transformers
- By default feed_type is 'CSV'
- It generates a batches folder inside test folder with the transformed output

```py
# for testing csv transformer
python3 test/test_transformers.py --feed_type=CSV

# for testing product transformer
python3 test/test_transformers.py --feed_type=PRODUCT

# for testing amg to sfcc location transformer
python3 test/test_transformers.py --feed_type=AMG_TO_SFCC_LOCATION
```

- To perform unit tests for all all transformer 

```py
# for unit testing all transformers
python3 test/test_all_transformers.py
```

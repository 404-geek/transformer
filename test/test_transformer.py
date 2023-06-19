from utils.tranformer.base_transformer import BaseTransformer


class TestTransformer(BaseTransformer):
    
    # Transform method which transforms the given chunk by following the given steps
    def transform(self, bucket_name: str, file_name: str, file_type: str, uuid: str, index: int, start: int, end: int, **kwargs) -> None:
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
        self.generate_batch(uuid, index, data, file_type, start)


    # add specified transformations to the given chunk
    def add_transformations(self, data):
        ''' Add required transformations here '''
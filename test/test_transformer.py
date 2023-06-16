from utils.base_transformer import BaseTransformer


class TestTransformer(BaseTransformer):
    
    # Transform method which transforms the given chunk by following the given steps
    def transform(self, s3_bucket: str, source: str, file_type: str, chunk_start: int, chunk_end: int, directory: str):
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
        

        ''' get data from s3 bucket '''
        data = self.get_data(s3_bucket, source, chunk_start, chunk_end)


        ''' validate the data chunk if required '''


        ''' add transformations to the chunk accordingly '''
        data = self.add_transformations(data)


        ''' remove any additional added tags while validating the chunk '''
        

        ''' generate batch file for the given chunk after transformations '''
        self.generate_batch(directory, data, file_type, chunk_start, chunk_end)


    # add specified transformations to the given chunk
    def add_transformations(self, data):
        ''' Add required transformations here '''
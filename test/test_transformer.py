from utils.base_tranformer import BaseTransformer


class TestTransformer(BaseTransformer):
    
    def transform(self, *args, **kwargs):

        # get arguments
        source = kwargs['source']
        file_type = kwargs['file_type']
        chunk_start = kwargs['chunk_start']
        chunk_end = kwargs['chunk_end']
        s3_bucket = kwargs['s3_bucket']
        directory = kwargs['directory']

        # get data from s3 bucket
        data = self.get_data(s3_bucket, source, chunk_start, chunk_end)


        # validate the data chunk if required


        # add transformations to the chunk accordingly
        data = self.add_transformations(data)


        # remove any additional added tags while validating the chunk
        

        # generate batch file for the given chunk after transformations
        self.generate_batch(directory, data, file_type, chunk_start, chunk_end)

    
    def add_transformations(self, *args, **kwargs):
        pass
from utils.base_transformer import BaseTransformer
import pandas as pd
from io import StringIO


class CsvTransformer(BaseTransformer):

    def transform(self, s3_bucket: str, source: str, file_type: str, chunk_start: int, chunk_end: int, directory: str) -> None:
        '''
            Tranform the given chunk by following the given steps
            
            - Fetch data from s3 bucket using get_data method which takes 
              s3_bucket, source, chunk_start, and chunk_end as arguments
            - Add specified transformations for the transformer in add_transformations method
            - Generate a batch file for the given chunk using generate_batch method which takes
              directory, data, file_type, chunk_start, and chunk_end as arguments

        '''

        # get data from s3 bucket
        data_string = self.get_data(s3_bucket, source, chunk_start, chunk_end)

        data_file = StringIO(data_string)
        if chunk_start != 0:
            column_names = ['STORE', 'QTY', 'VAL', 'BARCODE', 'DATE']
            data = pd.read_csv(data_file, names=column_names)
        else:
            data = pd.read_csv(data_file)

        # add specified transformations
        data = self.add_transformations(data)

        # generate a batch file for given chunk
        self.generate_batch(directory, data, file_type, chunk_start, chunk_end)


    def add_transformations(self, data:pd.DataFrame) -> pd.DataFrame:
        ''' Add required transformations here '''

        start_index=0
        data['Transaction Line'] = data.index + 1 + start_index
        data['Transaction Date'] = pd.to_datetime(data['DATE'], format="%Y%m%d").dt.strftime('%Y-%m-%d %H:%M:%S')
        data['Location Code'] = data['STORE'].astype(str).str.zfill(5)
        data['Is Price Override'] = 0
        data['Is Markup'] = 0
        data.rename(columns={"QTY":'Units', 'VAL':'Sold at Price', 'BARCODE':'UPC Number'}, inplace=True)
        data.drop(columns=['STORE', 'DATE'], inplace=True)
        return data
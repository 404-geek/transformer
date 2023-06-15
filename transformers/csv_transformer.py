from utils.base_tranformer import BaseTransformer
import pandas as pd
from io import StringIO


class CsvTransformer(BaseTransformer):

    def transform(self, *args, **kwargs):

        source = kwargs['source']
        file_type = kwargs['file_type']
        chunk_start = kwargs['chunk_start']
        chunk_end = kwargs['chunk_end']
        s3_bucket = kwargs['s3_bucket']
        directory = kwargs['directory']

        data_string = self.get_data(s3_bucket, source, chunk_start, chunk_end)

        data_file = StringIO(data_string)
        if chunk_start != 0:
            column_names = ['STORE', 'QTY', 'VAL', 'BARCODE', 'DATE']
            data = pd.read_csv(data_file, names=column_names)
        else:
            data = pd.read_csv(data_file)

        data = self.add_transformations(data)

        self.generate_batch(directory, data, file_type, chunk_start, chunk_end)


    def add_transformations(self, data:pd.DataFrame)->pd.DataFrame:
        start_index=0
        data['Transaction Line'] = data.index + 1 + start_index
        data['Transaction Date'] = pd.to_datetime(data['DATE'], format="%Y%m%d").dt.strftime('%Y-%m-%d %H:%M:%S')
        data['Location Code'] = data['STORE'].astype(str).str.zfill(5)
        data['Is Price Override'] = 0
        data['Is Markup'] = 0
        data.rename(columns={"QTY":'Units', 'VAL':'Sold at Price', 'BARCODE':'UPC Number'}, inplace=True)
        data.drop(columns=['STORE', 'DATE'], inplace=True)
        return data
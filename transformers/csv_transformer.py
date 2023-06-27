from utils.transformer.base_transformer import BaseTransformer
import pandas as pd


class CsvTransformer(BaseTransformer):

    def add_transformations(self, data: object) -> object:
        ''' Add required transformations here '''

        if not isinstance(data, pd.DataFrame):
            return data

        start_index=0
        data['Transaction Line'] = data.index + 1 + start_index
        data['Transaction Date'] = pd.to_datetime(data['DATE'], format="%Y%m%d").dt.strftime('%Y-%m-%d %H:%M:%S')
        data['Location Code'] = data['STORE'].astype(str).str.zfill(5)
        data['Is Price Override'] = 0
        data['Is Markup'] = 0
        data.rename(columns={"QTY":'Units', 'VAL':'Sold at Price', 'BARCODE':'UPC Number'}, inplace=True)
        data.drop(columns=['STORE', 'DATE'], inplace=True)
        return data
import unittest
from io import StringIO
import xml.etree.ElementTree as ET
import argparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transformers.transformer_factory import TransformerFactory


FEED_TYPE = 'CSV'

class TestTransformers(unittest.TestCase):

    def test_transformers(self):

        global FEED_TYPE

        trasformer = TransformerFactory.get_transformer(FEED_TYPE)
        directory = 'test/batches'

        if(FEED_TYPE == 'CSV'):
            data = StringIO("STORE,QTY,VAL,BARCODE,DATE\n1,2,3,1234,20230303")
            data = data.getvalue()
            source_file_type = 'csv'
            destination_file_type = 'csv'
            start = 0
            last = False
            uuid = 'test_csv_transformer'
            transformed_data = trasformer.get_transformed_chunk(data, source_file_type=source_file_type, destination_file_type=destination_file_type, start=start, last=last)
 
        elif(FEED_TYPE == 'PRODUCT'):
            data = "<products><product><upc>123</upc><step-quantity>1</step-quantity></product></products>"
            source_file_type = 'xml'
            destination_file_type = 'xml'
            start = 0
            last = False
            uuid = 'test_product_transformer'
            transformed_data = trasformer.get_transformed_chunk(data, source_file_type=source_file_type, destination_file_type=destination_file_type, start=start, last=last)

        elif(FEED_TYPE == 'AMG_TO_SFCC_LOCATION'):
            data = StringIO("Code,CompanyName,Type,Name,Address1,Address2,City,State,PostalCode,Country,Latitude,Longitude,Phone,Fax,Email,URL,Active,AllowsPickup,DropShipper,ShipPriority,GroupId,OpenOrderThreshold,Unnamed: 22,MaxOrderThreshold,Unnamed: 24,ReceiveCustomerBackOrderPOFlag\n1,Company1,Type1,Name1,Address1,Address2,City,State,12345,US,12.34,-56.78,1234567890,0987654321,email@example.com,http://example.com,1,1,1,1,1,1,1,1,1,1\n1,Company1,Type1,Name1,Address1,Address2,City,State,12345,US,12.34,-56.78,1234567890,0987654321,email@example.com,http://example.com,1,1,1,1,1,1,1,1,1,1")
            data = data.getvalue()
            source_file_type = 'csv'
            destination_file_type = 'xml'
            start = 0
            last = False
            uuid = 'test_amg_to_sfcc_location_transformer'
            transformed_data = trasformer.get_transformed_chunk(data, source_file_type=source_file_type, destination_file_type=destination_file_type, start=start, last=last)
        
        try:
            trasformer.generate_batch(data=transformed_data, directory=directory, uuid=uuid, index=0, destination_file_type=destination_file_type, start=start)
        except:
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--feed_type", help="Set the feed type", default='CSV')
    
    args, unknown = parser.parse_known_args()

    FEED_TYPE = args.feed_type

    unittest.main(argv=[sys.argv[0]] + unknown)
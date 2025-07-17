import pandas as pd
import boto3
from utils.transformer.base_transformer import BaseTransformer
from io import StringIO
import xml.etree.ElementTree as ET
import datetime
# from utils.transformer.amg_to_sfcc_list_and_sale_price_utils import getColumnsNames, getHeaderTag, getFileInfo, jurisdictions, getheaderChild, ns_uri, mapping

class ListAndSalePriceTransformer(BaseTransformer):
    def add_transformations(self, data: object, **kwargs):
        print('add_transformations')
        '''
        if not data:
            return data
        start = kwargs["start"]
        last = kwargs["last"]
        if start == 0:
            print("before reading data")
            print(data)
            data = pd.read_csv(data)
            print("after reading data")
            print(data)
        else:
            data = getColumnsNames(file_name, data)
            print(data)
            print("line 33 transformer")
        root = None
        
        if start == 0  : # either for first split or for single complete file
            date = datetime.datetime.today()
            root = ET.Element('pricebooks', {'xmlns': f'{ns_uri}{date.strftime("%Y-%m-%d")}'})
            headers = ET.SubElement(root, 'header', {"pricebook-id": f'{file_name.replace(".go", "")}'})
            file_info = getFileInfo(file_name)
            getHeaderTag(headers, file_info["jurisdiction"], file_info["fileType"])
            
        price_tables = None    
        if start == 0:
            price_tables = ET.SubElement(root, 'price-tables')
        else :
            price_tables = ET.Element('price_tables')
            root = price_tables
        for index, row in data.iterrows():
            subPriceTable = ET.SubElement(price_tables, "price-table", {'product-id': str(row[mapping[file_info["fileType"]]['itemNumber']])})
            amount = ET.SubElement(subPriceTable, "amount", {"quantity": "1"})
            amount.text = str(row[mapping[file_info["fileType"]]['price']])
    
            
            tree = ET.ElementTree(root)
            #data = ET.tostring(tree.getroot(), encoding="UTF-8").decode("UTF-8")
            data = ET.tostring(tree)
            print(data)
            print("transformation data line 46")
            #data = data.to_xml()
        #tree.write('final_file.xml', encoding='utf-8', xml_declaration=True)
        '''
        return '<a>10</a>'

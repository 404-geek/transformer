from utils.base_transformer import BaseTransformer
from datetime import datetime
from lxml import etree
from lxml.etree import _Element


class ProductTransformer(BaseTransformer):

    def transform(self, s3_bucket: str, source: str, file_type: str, chunk_start: int, chunk_end: int, directory: str) -> None:
        '''
            Tranform the given chunk by following the given steps
            
            - Fetch data from s3 bucket using get_data method which takes 
              s3_bucket, source, chunk_start, and chunk_end as arguments
            - Validate the given xml chunk data
            - Add specified transformations for the xml in add_transformations method
            - Remove extra tags added to the xml chunk
            - Generate a batch file for the given chunk using generate_batch method which takes
              directory, data, file_type, chunk_start, and chunk_end as arguments

        '''

        # get data from s3 bucket
        data = self.get_data(s3_bucket, source, chunk_start, chunk_end)

        # validate the given chunk
        chunk_list = self.generate_valid_file(file_type, data.splitlines())

        added_lines = len(chunk_list) - len(data.splitlines())
        chunk_str = '\n'.join(chunk_list)
            

        xml_content_bytes = bytes(chunk_str, encoding='UTF-8')
        root = etree.fromstring(xml_content_bytes)

        # add specified transformations
        root = self.add_transformations(root)


        xml_string = etree.tostring(root, pretty_print=True).decode('utf-8')
        lines = xml_string.splitlines()

        # remove added tags from the chunk
        if len(lines):
            if '<root>' in lines[0] and '</root>' in lines[-1]:
                lines.pop(0)
                lines.pop()
            else:
                for _ in range(added_lines):
                    lines.pop()

        # generate a batch file for given chunk
        self.generate_batch(directory, lines, file_type, chunk_start, chunk_end)


    def add_transformations(self, root: _Element) -> _Element:
        ''' Add required transformations here '''
        
        ns = {"ns": "http://www.demandware.com/xml/impex/catalog/2006-10-31"}

        products = root.xpath('//ns:product', namespaces=ns)
        for product in products:
            datetime_tag = etree.Element('datetime')
            datetime_tag.text = str(datetime.now())
            product.append(datetime_tag)

            upc = product.find('ns:upc', ns)
            color = etree.Element('color')
            color.text = 'brown' if upc is not None and upc.text else 'black'
            product.append(color)

            step_quantity = product.find('ns:step-quantity', ns)
            if step_quantity is not None and step_quantity.text == '1':
                order_fulfill = etree.Element('order-fulfill')
                order_fulfill.text = 'ordered'
                product.append(order_fulfill)

        return root





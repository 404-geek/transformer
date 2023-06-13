from lxml import etree
from datetime import datetime
from utils.base_tranformer import BaseTransformer
import boto3



class ProductTransformer(BaseTransformer):

    def transform(self, source, file_type, chunk_start, chunk_end, s3_bucket, directory):
        data = self.get_data(s3_bucket, source, chunk_start, chunk_end)

        chunk_list = self.generate_valid_file(file_type, data.splitlines())
        added_lines = len(chunk_list) - len(data.splitlines())


        chunk_str = '\n'.join(chunk_list)
            

        xml_content_bytes = bytes(chunk_str, encoding='UTF-8')
        root = etree.fromstring(xml_content_bytes)

        root = self.add_transformations(root)


        xml_string = etree.tostring(root, pretty_print=True).decode('utf-8')
        lines = xml_string.splitlines()

        if len(lines):
            if '<root>' in lines[0] and '</root>' in lines[-1]:
                lines.pop(0)
                lines.pop()
            else:
                for _ in range(added_lines):
                    lines.pop()

        
        self.generate_batch(directory, lines, file_type, chunk_start, chunk_end)


    def add_transformations(self, root):
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





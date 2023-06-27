from utils.transformer.base_transformer import BaseTransformer
from datetime import datetime
import xml.etree.ElementTree as ET



class ProductTransformer(BaseTransformer):

    def add_transformations(self, data: object) -> object:
        ''' Add required transformations here '''

        if not isinstance(data, ET.Element):
            return data
        
        ns = {"ns": "http://www.demandware.com/xml/impex/catalog/2006-10-31"}

        products = data.findall('.//ns:product', namespaces=ns)
        for product in products:
            datetime_tag = ET.Element('datetime')
            datetime_tag.text = str(datetime.now())
            product.append(datetime_tag)

            upc = product.find('ns:upc', ns)
            color = ET.Element('color')
            color.text = 'brown' if upc is not None and upc.text else 'black'
            product.append(color)

            step_quantity = product.find('ns:step-quantity', ns)
            if step_quantity is not None and step_quantity.text == '1':
                order_fulfill = ET.Element('order-fulfill')
                order_fulfill.text = 'ordered'
                product.append(order_fulfill)

        return data

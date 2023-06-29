from utils.transformer.base_transformer import BaseTransformer
from datetime import datetime
import xml.etree.ElementTree as ET



class ProductTransformer(BaseTransformer):

    def add_transformations(self, data: object, **kwargs) -> object:
        ''' Add required transformations here '''

        if not isinstance(data, ET.Element):
            return data
        
        products = data.findall('.//product')
        for product in products:
            datetime_tag = ET.Element('datetime')
            datetime_tag.text = str(datetime.now())
            product.append(datetime_tag)

            upc = product.find('upc')
            color = ET.Element('color')
            color.text = 'brown' if upc is not None and upc.text else 'black'
            product.append(color)

            step_quantity = product.find('step-quantity')
            if step_quantity is not None and step_quantity.text == '1':
                order_fulfill = ET.Element('order-fulfill')
                order_fulfill.text = 'ordered'
                product.append(order_fulfill)

        return data

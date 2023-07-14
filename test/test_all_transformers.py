import unittest
from io import StringIO
import xml.etree.ElementTree as ET
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transformers.transformer_factory import TransformerFactory



class TestTransformerFactory(unittest.TestCase):

    def setUp(self):
        self.transformer_factory = TransformerFactory()
    
    def test_invalid_transformers(self):
        with self.assertRaises(ValueError):
            self.transformer_factory.get_transformer('INVALID')
        with self.assertRaises(TypeError):
            self.transformer_factory.get_transformer()


class TestStoreTransformer(unittest.TestCase):

    def setUp(self):
        self.transformer = TransformerFactory().get_transformer('STORE')

    def test_add_transformations_with_valid_data(self):
        data = StringIO("STORE,QTY,VAL,BARCODE,DATE\n1,2,3,1234,20230303")
        transformed_data = self.transformer.add_transformations(data, start=0, last=True)
        expected_output = 'Units,Sold at Price,UPC Number,Transaction Line,Transaction Date,Location Code,Is Price Override,Is Markup\n2,3,1234,1,2023-03-03 00:00:00,00001,0,0\n'
        self.assertEqual(transformed_data, expected_output)

    def test_add_transformations_with_start_not_zero(self):
        data = StringIO("1,2,3,1234,20230303")
        transformed_data = self.transformer.add_transformations(data, start=1, last=True)
        expected_output = '2,3,1234,1,2023-03-03 00:00:00,00001,0,0\n'
        self.assertEqual(transformed_data, expected_output)

    def test_add_transformations_with_invalid_data(self):
        with self.assertRaises(FileNotFoundError):
            self.transformer.add_transformations("invalid_csv", start=0, last=True)
        self.assertEqual(self.transformer.add_transformations(None, start=0, last=True), None)


class TestProductTransformer(unittest.TestCase):

    def setUp(self):
        self.transformer = TransformerFactory().get_transformer('PRODUCT')

    def test_add_transformations_with_valid_xml(self):
        xml_data = "<products><product><upc>123</upc><step-quantity>1</step-quantity></product></products>"
        root = ET.fromstring(xml_data)
        transformed_data = self.transformer.add_transformations(root, start=0, last=True)
        root = ET.fromstring(transformed_data)
        self.assertIsNotNone(root.find('.//datetime'))
        self.assertIsNotNone(root.find('.//color'))
        self.assertIsNotNone(root.find('.//order-fulfill'))
        

    def test_add_transformations_with_invalid_xml(self):
        self.assertEqual(self.transformer.add_transformations("invalid_xml", start=0, last=True), "invalid_xml")
        self.assertEqual(self.transformer.add_transformations(None, start=0, last=True), None)


class TestAMGtoSFCCLocationTransformer(unittest.TestCase):

    def setUp(self):
        self.transformer = TransformerFactory().get_transformer('AMG_TO_SFCC_LOCATION')

    def test_transform_store_id_with_valid_data(self):
        self.assertEqual(self.transformer.transform_store_id('00001'), 'DC01')
        self.assertEqual(self.transformer.transform_store_id('00010'), 'DC10')
        self.assertEqual(self.transformer.transform_store_id('00960'), '960')
        self.assertEqual(self.transformer.transform_store_id(960), '960')
        self.assertEqual(self.transformer.transform_store_id(1), 'DC01')
        self.assertEqual(self.transformer.transform_store_id(10), 'DC10')

    def test_transform_store_id_with_invalid_data(self):
        with self.assertRaises(ValueError):
            self.transformer.transform_store_id('abcd')
        with self.assertRaises(ValueError):
            self.transformer.transform_store_id('abcd')
        with self.assertRaises(ValueError):
            self.transformer.transform_store_id('abcd')


    def test_add_transformations_with_valid_data(self):
        data = StringIO("Code,CompanyName,Type,Name,Address1,Address2,City,State,PostalCode,Country,Latitude,Longitude,Phone,Fax,Email,URL,Active,AllowsPickup,DropShipper,ShipPriority,GroupId,OpenOrderThreshold,Unnamed: 22,MaxOrderThreshold,Unnamed: 24,ReceiveCustomerBackOrderPOFlag\n1,Company1,Type1,Name1,Address1,Address2,City,State,12345,US,12.34,-56.78,1234567890,0987654321,email@example.com,http://example.com,1,1,1,1,1,1,1,1,1,1")
        transformed_data = self.transformer.add_transformations(data, start=0, last=True)
        self.assertIn('<store-id>DC01</store-id>', transformed_data)
        self.assertIn('<name>Name1</name>', transformed_data)
        self.assertIn('<address1>Address1</address1>', transformed_data)
        self.assertNotIn('<CompanyName>', transformed_data)


    def test_add_transformations_with_invalid_data(self):
        with self.assertRaises(FileNotFoundError):
            self.transformer.add_transformations("invalid_csv", start=0, last=True)
        # with self.assertRaises(FileNotFoundError):
        self.assertEqual(self.transformer.add_transformations(None, start=0, last=True), None)


if __name__ == '__main__':
    unittest.main()
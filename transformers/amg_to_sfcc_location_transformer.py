
import pandas as pd

import boto3

from utils.transformer.base_transformer import BaseTransformer

from io import StringIO


# from utils.db.db import update_file_type


class AMGtoSFCCLocationTransformer(BaseTransformer):

    # required transformations for the csv file

    def add_transformations(self, data: object, **kwargs) -> str:

        if not data:
            return data
        
        try:
            start = kwargs["start"]
            last = kwargs["last"]

            if(start == 0):
                data = pd.read_csv(data)
            else:
                columns = ['Code', 'CompanyName', 'Type', 'Name', 'Address1', 'Address2',
                        'City', 'State', 'PostalCode', 'Country', 'Latitude', 'Longitude',
                        'Phone', 'Fax', 'Email', 'URL', 'Active', 'AllowsPickup',
                        'DropShipper', 'ShipPriority', 'GroupId', 'OpenOrderThreshold', 'Unnamed: 22', 'MaxOrderThreshold',
                        'Unnamed: 24', 'ReceiveCustomerBackOrderPOFlag']
                data = pd.read_csv(data, names=columns)
        except Exception as e:
            raise(e)


        # Create a dictionary to map old column names to new column names

        column_mapping = {

            'Code': 'store-id',

            'Name': 'name',

            'Address1': 'address1',

            'Address2': 'address2',

            'City': 'city',

            'PostalCode': 'postal-code',

            'Country': 'country-code',

            'Phone': 'phone',

            'Email': 'email',

            'Latitude': 'latitude',

            'Longitude': 'longitude'

        }

        # Rename columns

        data.rename(columns=column_mapping, inplace=True)

        # Delete remaining columns

        columns_to_delete = data.columns.tolist()[15:]  # Exclude the renamed columns

        data.drop(columns=columns_to_delete, inplace=True)

        # Delete unwanted columns that in betwen the required columns, as per source file given

        columns_to_drop = ['Type', 'CompanyName', 'State', 'Fax']

        data.drop(columns=columns_to_drop, inplace=True)

        # store-id column for transformation

        data['store-id'] = data['store-id'].apply(self.transform_store_id)

        # convert and return the data into str format
        data = data.to_xml()

        if len(data):
            data = data.splitlines()
            if start != 0:
                if '<?xml' in data[0]:
                    del data[0]
                del data[0]
            if not last:
                del data[-1]
            data = '\n'.join(data)

        return data

        
    # store-id transformation function

    def transform_store_id(self, store_id: object) -> str:

        try:

            store_id_str = str(store_id)

            # if Store numbers between 1-99 in AMG denotes a “DC”. Therefore pad the “store number” with “DC” and last two digits of the AMG number before exporting to the other systems. e.g. 00001 = DC01

            if store_id_str.isdigit() and 1 <= int(store_id_str) <= 9:

                return "DC" + str(int(store_id_str)).zfill(2)

            elif store_id_str.isdigit() and 10 <= int(store_id_str) <= 99:

                return "DC" + str(int(store_id_str)).lstrip('0')

            # To remove the preceding zeroes when exporting from AMG to the other systems. e.g. 00960 = 960"

            else:

                return str(int(store_id_str)).lstrip('0')
        except Exception as e:
            print("Error: %s" % e)
            raise
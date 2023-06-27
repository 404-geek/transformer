from abc import ABC, abstractmethod
from utils.db.db import update_db
import xml.etree.ElementTree as ET
from typing import List
import pandas as pd
from io import StringIO
import boto3
import os


class BaseTransformer(ABC):

    @abstractmethod
    def add_transformations(self, **kwargs):
        ''' Interface method '''


    def generate_valid_xml_file(self, lines: List[str]) -> List[str]:
        ''' Generate valid xml file for the given chunk data '''

        open_tags = []
        new_lines = []

        for line in lines:
            stripped_line = line.strip()

            if stripped_line.startswith("<") and not stripped_line.startswith("</") and not stripped_line.endswith("/>"):
                if stripped_line.startswith("<?xml"):
                    new_lines.append(line)
                    continue

                tag = stripped_line.split()[0][1:]

                # Check if this line closes the tag
                if ">" in tag:
                    tag = tag.split(">")[0]

                if not stripped_line.endswith("</" + tag + ">"):
                    open_tags.append(tag)

                new_lines.append(line)
            
            elif stripped_line.startswith("</"):
                tag = stripped_line.split()[0][2:-1]

                while open_tags and open_tags[-1] != tag:
                    new_lines.append("</" + open_tags[-1] + ">\n")
                    open_tags.pop()

                if open_tags:
                    open_tags.pop()

                new_lines.append(line)
                
            else:
                new_lines.append(line)

        # Add remaining closing tags
        while open_tags:
            new_lines.append("</" + open_tags[-1] + ">\n")
            open_tags.pop()
        
        if len(new_lines) and '<?xml' not in new_lines[0]:
            new_lines.insert(0, '<root>')
            new_lines.append('</root>')


        return new_lines


    def generate_batch(self, directory: str, uuid: str, index: int, data, file_type: str, start: int) -> None:
        ''' Generate batch file for the given chunk data '''

        if not os.path.exists(directory):
            os.mkdir(directory)

        if not os.path.exists(f'{directory}/{uuid}'):
            os.mkdir(f'{directory}/{uuid}')

        batch_name = f'{directory}/{uuid}/{uuid}_{index}.txt'

        if file_type == 'xml':
            if len(data) and start == 0:
                data.insert(0, '<?xml version="1.0" encoding="UTF-8"?>')
        
            with open(batch_name, 'w') as f:
                f.write('\n'.join(data))
        else:
            data.to_csv(batch_name, index=False, header = (start == 0))

        update_db(batch_name)


    def get_data(self, bucket_name: str, file_name: str, start: int, end: int) -> str:
        ''' Fetch data from s3 bucket '''

        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name, Range=f'bytes={start}-{end}')
        data = response['Body'].read().decode('utf-8')
        return data
    

    def transform(self, bucket_name: str, file_name: str, file_type: str, uuid: str, index: int, start: int, end: int, directory: str, **kwargs):
        '''
            Tranform the given chunk by following the given steps
            
            - Fetch data from s3 bucket using get_data method which takes 
              bucket_name, file_name, start, and end as arguments
            - Get transformed chunk
            - Generate a batch file for the given chunk using generate_batch method which takes
              directory, data, file_type, start, and end as arguments

        '''

        # get data from s3 bucket
        data = self.get_data(bucket_name, file_name, start, end)

        # get transformed chunk
        data = self.get_transformed_chunk(data, file_type, start)

        # generate a batch file for given chunk
        self.generate_batch(directory, uuid, index, data, file_type, start)


    def get_transformed_chunk(self, data, file_type: str, start: int):
        '''
            Generate transformed data for the given chunk

            - Validate the given chunk data
            - Add specified transformations for the chunk in add_transformations method
            - Remove extra tags added to if file type is xml
        '''

        if(file_type == 'xml'):

            # validate the given chunk
            chunk_list = self.generate_valid_xml_file(data.splitlines())

            added_lines = len(chunk_list) - len(data.splitlines())
            chunk_str = '\n'.join(chunk_list)
                

            xml_content_bytes = bytes(chunk_str, encoding='UTF-8')
            root = ET.fromstring(xml_content_bytes)

            # add specified transformations
            root = self.add_transformations(data=root)


            xml_string = ET.tostring(root, encoding='unicode')
            lines = xml_string.splitlines()

            # remove added tags from the chunk
            if len(lines):
                if '<root>' in lines[0] and '</root>' in lines[-1]:
                    lines.pop(0)
                    lines.pop()
                else:
                    for _ in range(added_lines):
                        lines.pop()
            return lines
        
        else:

            data_file = StringIO(data)
            if start != 0:
                column_names = ['STORE', 'QTY', 'VAL', 'BARCODE', 'DATE']
                data = pd.read_csv(data_file, names=column_names)
            else:
                data = pd.read_csv(data_file)

            # add specified transformations
            data = self.add_transformations(data=data)

        
            return data

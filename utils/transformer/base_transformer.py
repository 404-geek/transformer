from abc import ABC, abstractmethod
from utils.db.db import update_db
from utils.utils import check_and_add_xml_header
import xml.etree.ElementTree as ET
from typing import List
import pandas as pd
from io import StringIO
import boto3
import os


class BaseTransformer(ABC):

    @abstractmethod
    def add_transformations(self, **kwargs) -> str:
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


    def is_valid_xml(self, lines: List[str]) -> bool:
        ''' Check if the given XML chunk is valid or not '''

        xml_string = "".join(lines)
        try:
            # Try to parse the XML string
            ET.fromstring(xml_string)
            return True
        except ET.ParseError:
            return False


    def generate_batch(self, directory: str, uuid: str, index: int, data: str, destination_file_type: str, start: int) -> None:
        ''' Generate batch file for the given chunk data '''

        if not os.path.exists(directory):
            os.mkdir(directory)

        if not os.path.exists(f'{directory}/{uuid}'):
            os.mkdir(f'{directory}/{uuid}')

        batch_name = f'{directory}/{uuid}/{uuid}_{index}.txt'


        data = data.splitlines()

        if destination_file_type == 'xml':
            data = check_and_add_xml_header(data, start)
        
        with open(batch_name, 'w') as f:
            f.write('\n'.join(data))

        update_db(index)


    def get_data(self, bucket_name: str, file_name: str, start: int, end: int) -> str:
        ''' Fetch data from s3 bucket '''

        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name, Range=f'bytes={start}-{end}')
        data = response['Body'].read().decode('utf-8')
        return data
    

    def transform(self, bucket_name: str, file_name: str, source_file_type: str, destination_file_type: str, uuid: str, index: int, start: int, end: int, directory: str, last: bool, **kwargs) -> None:
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
        data = self.get_transformed_chunk(data, source_file_type, destination_file_type, start, last)

        # generate a batch file for given chunk
        self.generate_batch(directory, uuid, index, data, destination_file_type, start)


    def get_transformed_chunk(self, data: str, source_file_type: str, destination_file_type: str, start: int, last: bool, **kwargs) -> str:
        '''
            Generate transformed data for the given chunk

            - Validate the given chunk data
            - Add specified transformations for the chunk in add_transformations method
            - Remove extra tags added to if file type is xml
        '''
        try:
            if(source_file_type == 'xml'):

                data_lines = data.splitlines()
                # check if xml chunk is valid or not
                valid_xml = self.is_valid_xml(data_lines)

                if(not valid_xml):
                    # validate the given chunk if it is not valid
                    chunk_list = self.generate_valid_xml_file(data_lines)
                else:
                    chunk_list = data_lines

                added_lines = len(chunk_list) - len(data_lines)
                chunk_str = '\n'.join(chunk_list)
                    

                xml_content_bytes = bytes(chunk_str, encoding='UTF-8')
                root = ET.fromstring(xml_content_bytes)

                # Remove namespaces from XML tags
                
                # for elem in root.getiterator():
                for elem in root.iter():
                    if not hasattr(elem.tag, 'find'): continue
                    i = elem.tag.find('}')
                    if i >= 0:
                        elem.tag = elem.tag[i + 1:]

                # add specified transformations
                data = self.add_transformations(data=root, start=start, last=last)

                if destination_file_type == 'xml':
                    lines = data.splitlines()

                    # remove added tags from the chunk
                    if len(lines):
                        if '<root>' in lines[0] and '</root>' in lines[-1]:
                            lines.pop(0)
                            lines.pop()

                        for _ in range(added_lines):
                            lines.pop()

                    # Convert the list of lines back to a single string
                    data = '\n'.join(lines)

                return data
            
            elif(source_file_type == 'csv'):

                data_file = StringIO(data)

                # add specified transformations
                data = self.add_transformations(data=data_file, start=start, last=last)

                if isinstance(data, StringIO):
                    data = data.getvalue()
                
                return data
        except:
            return data

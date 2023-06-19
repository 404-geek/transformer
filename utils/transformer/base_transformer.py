from abc import ABC, abstractmethod
from utils.db.db import update_db
from typing import List
import boto3
import os


class BaseTransformer(ABC):

    @abstractmethod
    def transform(self, **kwargs):
        ''' Interface method '''


    def generate_valid_xml_file(self, lines: List[str]) -> List[str]:
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
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name, Range=f'bytes={start}-{end}')
        data = response['Body'].read().decode('utf-8')
        return data
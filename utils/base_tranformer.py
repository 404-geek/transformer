from abc import ABC, abstractmethod
from typing import List
import boto3
import os


class BaseTransformer(ABC):

    @abstractmethod
    def transform():
        ''' Interface method '''


    def generate_valid_file(self, file_type: str, lines: List[str]) -> List[str]:
        file_generators = {
            "XML": self.generate_valid_xml,
            "CSV": self.generate_valid_csv
        }

        generate_file = file_generators.get(file_type)

        if generate_file is None:
            raise ValueError(f"Unsupported file type: {file_type}")

        return generate_file(lines)


    def make_valid_xml(self, lines):
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


    def make_valid_csv(self, lines):
        ''' Make Valid CSV  '''


    def generate_batch(self, directory, data, file_type, chunk_start, chunk_end):
        if not os.path.exists(directory):
            os.mkdir(directory)

        batch_name = f'{directory}/batch_{chunk_start}_{chunk_end}.txt'

        if len(data) and chunk_start == 0 and file_type == 'xml':
            data.insert(0, '<?xml version="1.0" encoding="UTF-8"?>')
    
            with open(batch_name, 'w') as f:
                f.write('\n'.join(data)) 
        else:
            data.to_csv(batch_name, index=False, header = (chunk_start == 0))


    def get_data(self, s3_bucket, source, chunk_start, chunk_end):
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=s3_bucket, Key=source, Range=f'bytes={chunk_start}-{chunk_end}')
        data = response['Body'].read().decode('utf-8')
        return data
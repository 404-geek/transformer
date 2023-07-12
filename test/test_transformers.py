import xml.etree.ElementTree as ET
from typing import List
import argparse
import logging
import ast
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transformers.transformer_factory import TransformerFactory


def get_test_data(source:str, start: int, end: int) -> str:
    try:
        with open(source, 'r') as file:
            file.seek(start)
            if end is None:  # If end is not specified, read to the end of the file.
                data = file.read()
            else:  # If end is specified, read the specified chunk.
                data = file.read(end - start)
        return data
    except Exception as e:
        print("Error: %s" % e)
        raise
    

def get_and_save_output(transformer, source: str, start: int or None, end: int or None, last: bool, source_file_type: str, destination_file_type: str, filename: str, **kwargs) -> None:
    data = get_test_data(source, start, end)
    # print(data, '---------------')
    transformed_data = transformer.get_transformed_chunk(data=data, start=start, last=last, source_file_type=source_file_type, destination_file_type=destination_file_type, **kwargs)
    with open(filename, 'w') as file:
        file.write(transformed_data)


def test_transformers(feed_type: str, split_points: List[int] or None, start: int or None, end: int or None, last: bool, source_file_type: str, destination_file_type: str, **kwargs) -> None:

    transformer = TransformerFactory.get_transformer(feed_type)

    directory = 'test'
    files = []
    try:
        for file in os.listdir(f'{directory}/input'):
            if os.path.isfile(os.path.join(f'{directory}/input', file)):
                files.append(file)
    except:
        return print("Error: No input folder provided inside test folder")

    if len(files) == 0:
        return print("Error: Please provide a input file inside input folder")

    if len(files) > 1:
        return print("Error: Please provide only one file inside input folder")

    if not os.path.exists(f'{directory}/output'):
        os.mkdir(f'{directory}/output')

    try:
        split = os.path.splitext(files[0])
        file_name = split[0]

        if source_file_type != split[1][1:]:
            raise ValueError("Invalid input file type")

        if not destination_file_type:
            destination_file_type = source_file_type
        source = f'{directory}/input/{files[0]}'

        if not split_points:
            output_file_name = f'{directory}/output/{file_name}_batch.txt'
            get_and_save_output(
                transformer=transformer, 
                source=source, 
                start=start, 
                end=end, 
                last=last, 
                source_file_type=source_file_type, 
                destination_file_type=destination_file_type, 
                filename=output_file_name,
                **kwargs
            )
        
        else:
            split_points.insert(0, 0)
            split_length = len(split_points)
            for i in range(split_length - 1):
                start = split_points[i]
                if i > 0:
                    start += 1
                end = split_points[i+1]
                last = (i == (split_length - 2))
                if not os.path.exists(f'{directory}/output/{file_name}'):
                    os.mkdir(f'{directory}/output/{file_name}')
                output_file_name = f'{directory}/output/{file_name}/{file_name}_batch_{i+1}.txt'
                get_and_save_output(
                    transformer=transformer, 
                    source=source, 
                    start=start, 
                    end=end, 
                    last=last, 
                    source_file_type=source_file_type, 
                    destination_file_type=destination_file_type, 
                    filename=output_file_name,
                    **kwargs
                )
    
    except NameError:
        return print("Error: Invalid input file")
    except Exception as e:
        print("Error: %s" % e)
        raise


def validate_args(args) -> dict:

    if not args['feed_type']:
        raise ValueError("feed_type is required")

    if not args['source_file_type']:
        raise ValueError("source_file_type is required")

    if not args['destination_file_type']:
        raise ValueError("destination_file_type is required")

    if not args['split_points']:
        if args['start'] and (not args['last']):
            raise ValueError("end or last=True is required")

        if (not args['start']) and (not args['end']):
            raise ValueError("Either (start and end) or split_points are required")

    try:
        if args['start'] is not None:
            args['start'] = int(args['start'])
        if args['end'] is not None:
            args['end'] = int(args['end'])
    except ValueError:
        raise ValueError("Invalid start/end type, it should be a number")

    if isinstance(args['last'], str):
        if args['last'].lower() == 'false':
            args['last'] = False
        elif args['last'].lower() == 'true':
            args['last'] = True
        else:
            raise ValueError("Invalid last type, it should be True or False")

    if args['split_points']:
        args['split_points'] = ast.literal_eval(args['split_points'])
        for split_point in args['split_points']:
            try:
                split_point = int(split_point)
            except ValueError:
                raise ValueError(f"Invalid split point: {split_point}")
        args['split_points'] = list(args['split_points'])

    return args


def main():
    args = sys.argv[1:]
    kwargs = {}

    for arg in args:
        if arg.startswith('--'):
            if '=' in arg:
                key, value = arg[2:].split('=')
                kwargs[key] = value
            else:
                kwargs[arg[2:]] = True

    try:
        validated_args = validate_args(kwargs)
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    test_transformers(**validated_args)


if __name__ == '__main__':
    main()

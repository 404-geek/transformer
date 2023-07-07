import xml.etree.ElementTree as ET
from typing import List
import argparse
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
    

def get_and_save_output(transformer, source: str, start: int or None, end: int or None, last: bool, source_file_type: str, destination_file_type: str, filename: str) -> None:
    data = get_test_data(source, start, end)
    # print(data, '---------------')
    transformed_data = transformer.get_transformed_chunk(data=data, start=start, last=last, source_file_type=source_file_type, destination_file_type=destination_file_type)
    with open(filename, 'w') as file:
        file.write(transformed_data)


def test_transformers(feed_type: str, split_points: List[int] or None, start: int or None, end: int or None, last: bool, destination_file_type: str) -> None:

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
        source_file_type = split[1][1:]
        if not destination_file_type:
            destination_file_type =source_file_type
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
                filename=output_file_name
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
                    filename=output_file_name
                )
    
    except NameError:
        return print("Error: Invalid input file")
    except Exception as e:
        print("Error: %s" % e)
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--feed_type", help="Set the feed type (str)")
    parser.add_argument("--start", help="Set start (int)", default=None)
    parser.add_argument("--end", help="Set end (int)", default=None)
    parser.add_argument("--last", help="Set last (bool)", default=False)
    parser.add_argument("--split_points", help="Set split points (int[])", default=None)
    parser.add_argument("--destination_file_type", help="Set destination file type (str)")

    
    args, unknown = parser.parse_known_args()

    feed_type = args.feed_type
    start = args.start
    end = args.end
    last = args.last
    split_points = args.split_points
    destination_file_type = args.destination_file_type

    if not split_points:
        if start and (not last):
            raise ValueError("end or last=True is required")

        if (not start) and (not end):
            raise ValueError("Either (start and end) or split_points are required")


    try:
        if start != None:
            start = int(start)
        if end != None:
            end = int(end)
    except:
        raise ValueError("Invalid start/end type, it should be a number")

    if isinstance(last, str):
        if last == 'False':
            last = False
        elif last == 'True':
            last = True
        else:
            raise ValueError("Invalid last type, it should be a True or False")
    

    if split_points:
        split_points_list = ast.literal_eval(split_points)
        for split_point in split_points_list:
            try:
                split_point = int(split_point)
            except ValueError:
                raise ValueError("Invalid split point: %s" % split_point)
        split_points_list = list(split_points_list)

            

    test_transformers(feed_type, split_points_list, start, end, last, destination_file_type)


if __name__ == '__main__':
    main()

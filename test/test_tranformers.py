import xml.etree.ElementTree as ET
import argparse
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
        return str(e)
    

def test_transformers(feed_type: str, start: int, end: int or None, last: bool, destination_file_type: str) -> None:

    trasformer = TransformerFactory.get_transformer(feed_type)

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
    

    try:
        split = os.path.splitext(files[0])
        file_name = split[0]
        source_file_type = split[1][1:]
        if not destination_file_type:
            destination_file_type =source_file_type
        source = f'{directory}/input/{files[0]}'
        data = get_test_data(source, start, end)
        trasformed_data = trasformer.get_transformed_chunk(data=data, start=start, last=last, source_file_type=source_file_type, destination_file_type=destination_file_type)
    except:
        return print("Error: Invalid input file")

    if not os.path.exists(f'{directory}/output'):
        os.mkdir(f'{directory}/output')

    with open(f'{directory}/output/{file_name}_batch.txt', 'w') as file:
        file.write(trasformed_data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--feed_type", help="Set the feed type (str)")
    parser.add_argument("--start", help="Set start (int)")
    parser.add_argument("--end", help="Set end (int)", default=None)
    parser.add_argument("--last", help="Set last (bool)")
    parser.add_argument("--destination_file_type", help="Set destination file type (str)")

    
    args, unknown = parser.parse_known_args()

    feed_type = args.feed_type
    try:
        start = int(args.start)
        if args.end != None:
            end = int(args.end)
        else:
            end = args.end
    except:
        return print("Error: Invalid start/end type, it should be a number")

    if isinstance(args.last, str):
        if args.last == 'False':
            last = False
        elif args.last == 'True':
            last = True
        else:
            return print("Error: Invalid last type, it should be a True or False")
    else:
        last = args.last
    
    destination_file_type = args.destination_file_type


    test_transformers(feed_type, start, end, last, destination_file_type)


if __name__ == '__main__':
    main()

import xml.etree.ElementTree as ET
import argparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transformers.transformer_factory import TransformerFactory


def test_transformers(feed_type: str, start: int, last: bool, destination_file_type: str) -> None:

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
    
    with open(f'{directory}/input/{files[0]}', 'r') as data:
        data = data.read()
        try:
            split = os.path.splitext(files[0])
            file_name = split[0]
            source_file_type = split[1][1:]
            if not destination_file_type:
                destination_file_type =source_file_type
            # trasformed_data = trasformer.add_transformations(data, start=start, last=last)
            # print(type(data), source_file_type)
            trasformed_data = trasformer.get_transformed_chunk(data=data, start=start, last=last, source_file_type=source_file_type, destination_file_type=destination_file_type)
            # print(trasformed_data, type(trasformed_data))
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
    parser.add_argument("--last", help="Set last (bool)")
    parser.add_argument("--destination_file_type", help="Set destination file type (str)")

    
    args, unknown = parser.parse_known_args()

    feed_type = args.feed_type
    try:
        start = int(args.start)
    except:
        return print("Error: Invalid start type, it should be a number")

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


    test_transformers(feed_type, start, last, destination_file_type)


if __name__ == '__main__':
    main()

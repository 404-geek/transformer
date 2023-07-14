from typing import List
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

    source_file_path = kwargs.get("source_file_path")
    destination_file_path = kwargs.get("destination_file_path")

    transformer = TransformerFactory.get_transformer(feed_type)

    try:
        directory, file_with_extension = os.path.split(source_file_path)
        file_name, file_format = os.path.splitext(file_with_extension)


        if source_file_type != file_format[1:]:
            raise ValueError("Invalid input file type")


        if not split_points:
            output_file_name = f'{destination_file_path}/{file_name}_batch.txt'
            get_and_save_output(
                transformer=transformer, 
                source=source_file_path, 
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
                if not os.path.exists(f'{destination_file_path}/{file_name}'):
                    os.mkdir(f'{destination_file_path}/{file_name}')
                output_file_name = f'{destination_file_path}/{file_name}/{file_name}_batch_{i+1}.txt'
                get_and_save_output(
                    transformer=transformer, 
                    source=source_file_path, 
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

    if not args.get('feed_type'):
        raise ValueError("feed_type is required")
    
    if not args.get('source_file_path'):
        raise ValueError("source_file_path is required")

    if not args.get('source_file_type'):
        raise ValueError("source_file_type is required")
    
    if not args.get('destination_file_path'):
        raise ValueError("destination_file_path is required")
    
    if not args.get('destination_file_type'):
        raise ValueError("destination_file_type is required")
    
    if not os.path.exists(args.get("source_file_path")):
        raise ValueError("Invalid source_file_path")
    
    if not os.path.exists(args.get("destination_file_path")):
        raise ValueError("Invalid destination_file_path")

    
    if isinstance(args.get('last'), str):
        if args.get('last').lower() == 'false':
            args['last'] = False
        elif args.get('last').lower() == 'true':
            args['last'] = True
        else:
            raise ValueError("Invalid last type, it should be True or False")
    else:
        args['last'] = False

    if not args.get('split_points'):
        args['split_points'] = None
        if args.get('start') and (not args.get('last')):
            raise ValueError("end or last=True is required")

        if (not args.get('start')) and (not args.get('end')):
            raise ValueError("Either (start and end) or split_points are required")
    else:
        args['split_points'] = ast.literal_eval(args.get('split_points'))
        for split_point in args['split_points']:
            try:
                split_point = int(split_point)
            except ValueError:
                raise ValueError(f"Invalid split point: {split_point}")
        args['split_points'] = list(args['split_points'])

    try:
        if args.get('start'):
            args['start'] = int(args.get('start'))
        else:
            args['start'] = None
        if args.get('end'):
            args['end'] = int(args.get('end'))
        else:
            args['end'] = None
    except ValueError:
        raise ValueError("Invalid start/end type, it should be a number")


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

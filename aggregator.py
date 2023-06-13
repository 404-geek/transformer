from kafka import KafkaConsumer
from config.config import KAFKA_SERVER, AGGREGATOR_CHANNEL
import json
import os




def aggregator(byte_ranges, file_name, file_type, directory):
    with open(f'{file_name}_transformed.{file_type}', "w") as final_file:

        for i in range(len(byte_ranges)-1):
            start = byte_ranges[i]
            if i > 0:
                start = start + 1
            end = byte_ranges[i+1]
            batch_name = f'{directory}/batch_{start}_{end}.txt'
            with open(batch_name, "r") as f:
                contents = f.read()

            final_file.write(contents)


def main():
    consumer = KafkaConsumer(AGGREGATOR_CHANNEL, bootstrap_servers=KAFKA_SERVER)

    for message in consumer:
        data = json.loads(message.value.decode('utf-8'))
        byte_ranges = data['byte_ranges']
        file_type = data['file_type']
        file_name = data['file_name']
        directory = data['directory']

        while True:
            files = os.listdir(directory)
            if len(files) == len(byte_ranges) - 1:
                aggregator(byte_ranges, file_name, file_type, directory)
                break


main()


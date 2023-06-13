from kafka import KafkaProducer
from config.config import KAFKA_SERVER, TRANSFORMER_CHANNEL, AGGREGATOR_CHANNEL
import json


DIRECTORY = 'batches'
S3_BUCKET = 'test-stride'

# SOURCE = 'DEMANDWAREmasterCatalog_P8_20221102160230.xml'
# FILE_NAME = 'DEMANDWAREmasterCatalog_P8_20221102160230'
# FEED_TYPE = 'PRODUCT'
# FILE_TYPE = 'xml'

SOURCE = 'test.csv'
FILE_NAME = 'test'
FEED_TYPE = 'CSV'
FILE_TYPE = 'csv'


producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

# byte_ranges = [0, 17715066, 35428650, 53141394, 70856158, 88570444, 106283396, 123996049, 141711336, 159424875]
byte_ranges = [0, 249777784, 499555588, 749333369, 999111150, 1248888906, 1498666703, 1748444493, 1998222274, 2248000027]

for i in range(len(byte_ranges) - 1):
    start = byte_ranges[i]
    if i > 0:
        start = start + 1
    end = byte_ranges[i+1]

    range_dict = {
        "start": start, 
        "end": end, 
        "feed_type": FEED_TYPE, 
        "source": SOURCE,
        's3_bucket': S3_BUCKET,
        'directory': DIRECTORY,
        'file_type': FILE_TYPE
    }
    range_bytes = json.dumps(range_dict).encode('utf-8')
    producer.send(TRANSFORMER_CHANNEL, range_bytes)

aggregator_dict = {
    'byte_ranges': byte_ranges,
    'file_type': FILE_TYPE,
    'file_name': FILE_NAME,
    'directory': DIRECTORY,
}
producer.send(AGGREGATOR_CHANNEL, json.dumps(aggregator_dict).encode('utf-8'))

producer.close()
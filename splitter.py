from kafka import KafkaProducer
from config.config import KAFKA_SERVER, TRANSFORMER_CHANNEL, AGGREGATOR_CHANNEL
import json

UUID = '209af911-630a-425f-8e09-c005452e2556'

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

file_name = 'albertron-sale-2.csv'
source_file_type = 'csv'
destination_file_type = 'csv'
byte_ranges = [0, 249777783, 499555587, 749333368, 999111149, 1248888905, 1498666702, 1748444492, 1998222273, 2248000027]
# byte_ranges = [0, 5026, 10056]
feed_type ='CSV'

# file_name = 'DEMANDWAREmasterCatalog_P8_20221102160230.xml'
# source_file_type = 'xml'
# destination_file_type = 'xml'
# byte_ranges = [0, 17715066, 35428650, 53141394, 70856158, 88570444, 106283396, 123996049, 141711336, 159424875]
# feed_type = 'PRODUCT'

for i in range(len(byte_ranges) - 1):
    start = byte_ranges[i]
    if i > 0:
        start = start + 1
    end = byte_ranges[i+1]


    range_dict = {
        "feed_type": feed_type,
        "uuid": UUID,
        "event": "transform",
        "bucket_name": "test-stride",
        "file_name": file_name,
        "source_file_type": source_file_type,
        "destination_file_type": destination_file_type,
        "start": start,
        "end": end,
        "index": i,
        "last": i == len(byte_ranges) - 1,
        "directory": "batches"
    }
    range_bytes = json.dumps(range_dict).encode('utf-8')
    producer.send(TRANSFORMER_CHANNEL, range_bytes)

aggregator_dict = {
    'byte_ranges': byte_ranges,
    'file_type': "csv",
    'file_name': "albertron-sale-2.csv",
    "uuid": UUID
}
producer.send(AGGREGATOR_CHANNEL, json.dumps(aggregator_dict).encode('utf-8'))

producer.close()
from kafka import KafkaProducer
from config.config import KAFKA_SERVER, TRANSFORMER_CHANNEL, AGGREGATOR_CHANNEL
import json

UUID = '209af911-630a-425f-8e09-c005452e2556'

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

byte_ranges = [0, 249777783, 499555587, 749333368, 999111149, 1248888905, 1498666702, 1748444492, 1998222273, 2248000027]

for i in range(len(byte_ranges) - 1):
    start = byte_ranges[i]
    if i > 0:
        start = start + 1
    end = byte_ranges[i+1]


    range_dict = {
        "feed_type": "CSV",
        "uuid": UUID,
        "event": "transform",
        "bucket_name": "test-stride",
        "file_name": "albertron-sale-2.csv",
        "file_type": "csv",
        "start": start,
        "end": end,
        "index": i,
        "last": i == len(byte_ranges) - 1,
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
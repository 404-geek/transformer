from transformers.transformer_factory import TransformerFactory
from kafka import KafkaConsumer
from config.config import KAFKA_SERVER, TRANSFORMER_CHANNEL
import json



def main():
    
    consumer = KafkaConsumer(TRANSFORMER_CHANNEL, bootstrap_servers=KAFKA_SERVER)

    for message in consumer:
        data = json.loads(message.value.decode('utf-8'))
        feed_type = data['feed_type']
        uuid = data['uuid']
        event = data['event']
        bucket_name = data['bucket_name']
        file_name = data['file_name']
        file_type = data['file_type']
        start = data['start']
        end = data['end']
        index = data['index']
        last = data['last']

        transformer = TransformerFactory.get_transformer(feed_type)
        transformer.transform(
            bucket_name=bucket_name, 
            file_name=file_name, 
            file_type=file_type, 
            uuid=uuid,
            index=index,
            start=start, 
            end=end, 
        )

    consumer.close()

main()
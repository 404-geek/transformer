from transformers.transformer_factory import TransformerFactory
from kafka import KafkaConsumer
from config.config import KAFKA_SERVER, TRANSFORMER_CHANNEL
from utils.exception_handler.handler import setup_logger, log_error
import json



def main():
    
    setup_logger()

    consumer = KafkaConsumer(TRANSFORMER_CHANNEL, bootstrap_servers=KAFKA_SERVER)

    for message in consumer:
        data = json.loads(message.value.decode('utf-8'))
        feed_type = data['feed_type']
        uuid = data['uuid']
        event = data['event']
        bucket_name = data['bucket_name']
        file_name = data['file_name']
        source_file_type = data['source_file_type']
        destination_file_type = data['destination_file_type']
        start = data['start']
        end = data['end']
        index = data['index']
        last = data['last']
        directory = data['directory']

        transformer = TransformerFactory.get_transformer(feed_type)
        
        try:
            transformer.transform(
                bucket_name=bucket_name, 
                file_name=file_name, 
                source_file_type=source_file_type, 
                destination_file_type=destination_file_type, 
                uuid=uuid,
                index=index,
                start=start, 
                end=end, 
                directory=directory,
                last=last
            )
        except Exception as e:
            log_error(e, file_name, uuid, start, end)

    consumer.close()

main()
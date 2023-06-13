from transformers.transformer_factory import TranformerFactory
from kafka import KafkaConsumer
from config.config import KAFKA_SERVER, TRANSFORMER_CHANNEL
import json



def main():
    
    consumer = KafkaConsumer(TRANSFORMER_CHANNEL, bootstrap_servers=KAFKA_SERVER)

    for message in consumer:
        data = json.loads(message.value.decode('utf-8'))
        start = data['start']
        end = data['end']
        feed_type = data['feed_type']
        source = data['source']
        s3_bucket = data['s3_bucket']
        directory = data['directory']
        file_type = data['file_type']

        print("yes")

        transformer = TranformerFactory.get_transformer(feed_type)
        transformer.transform(source, file_type, start, end, s3_bucket, directory)


    consumer.close()


main()
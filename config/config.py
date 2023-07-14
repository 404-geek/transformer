from environs import Env
import json

env = Env()
env.read_env()


KAFKA_SERVER = env.str("KAFKA_SERVER")

TRANSFORMER_CHANNEL=env.str("TRANSFORMER_CHANNEL")
AGGREGATOR_CHANNEL=env.str("AGGREGATOR_CHANNEL")

DYNAMODB_KEY=env.str("DYNAMODB_KEY")


def get_integrations(feed_type: str):
    integrations_file_path = 'config/integrations.json'
    with open(integrations_file_path, 'r') as file:
        data = json.load(file)
    return data[feed_type]
from environs import Env
import json

env = Env()
env.read_env()


KAFKA_SERVER = env.str("KAFKA_SERVER")

TRANSFORMER_CHANNEL=env.str("TRANSFORMER_CHANNEL")
AGGREGATOR_CHANNEL=env.str("AGGREGATOR_CHANNEL")

DYNAMODB_KEY=env.str("DYNAMODB_KEY")

API_URI=env.str("API_URI")

DB_HOST=env.str("DB_HOST")
DB_NAME=env.str("DB_NAME")
DB_USER=env.str("DB_USER")
DB_PASSWORD=env.str("DB_PASSWORD")


def get_integrations(feed_type: str):
    integrations_file_path = 'config/integrations.json'
    with open(integrations_file_path, 'r') as file:
        data = json.load(file)
    return data[feed_type]
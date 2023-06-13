from environs import Env

env = Env()
env.read_env()


KAFKA_SERVER = env.str("KAFKA_SERVER")

TRANSFORMER_CHANNEL=env.str("TRANSFORMER_CHANNEL")
AGGREGATOR_CHANNEL=env.str("AGGREGATOR_CHANNEL")
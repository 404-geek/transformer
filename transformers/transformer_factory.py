from transformers.product_transformer import ProductTransformer
from transformers.csv_transformer import CsvTransformer
from test.test_transformer import TestTransformer


class TransformerFactory:

    _transformers = {}

    @staticmethod
    def register_transformer(key, transformer):
        TransformerFactory._transformers[key] = transformer

    @staticmethod
    def get_transformer(feed_type):
        transformer = TransformerFactory._transformers.get(feed_type)
        if transformer:
            return transformer()
        else:
            raise ValueError(f"Unsupported feed type: {feed_type}")


# Registering transformers
TransformerFactory.register_transformer("PRODUCT", ProductTransformer)
TransformerFactory.register_transformer("CSV", CsvTransformer)
TransformerFactory.register_transformer("TEST", TestTransformer)
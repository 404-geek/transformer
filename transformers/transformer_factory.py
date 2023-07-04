from transformers.product_transformer import ProductTransformer
from transformers.csv_transformer import CsvTransformer
from transformers.amg_to_sfcc_location_transformer import AMGtoSFCCLocationTransformer
from transformers.sample_transformer import SampleTransformer
from utils.transformer.base_transformer import BaseTransformer
from typing import Type


TransformerType = Type[BaseTransformer]

class TransformerFactory:

    _transformers = {}

    # register a transformer
    @staticmethod
    def register_transformer(key:str, transformer: TransformerType) -> None:
        ''' Registering a transformer using feed type'''

        TransformerFactory._transformers[key] = transformer


    # get transformer based on feed type
    @staticmethod
    def get_transformer(feed_type:str) -> BaseTransformer :
        ''' Get required transformer based on feed type '''

        transformer = TransformerFactory._transformers.get(feed_type)
        if transformer:
            return transformer()
        else:
            raise ValueError(f"Unsupported feed type: {feed_type}")



# Registering transformers
TransformerFactory.register_transformer("PRODUCT", ProductTransformer)
TransformerFactory.register_transformer("CSV", CsvTransformer)
TransformerFactory.register_transformer("AMG_TO_SFCC_LOCATION", AMGtoSFCCLocationTransformer)
TransformerFactory.register_transformer("SAMPLE", SampleTransformer)
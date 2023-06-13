from transformers.product_transformer import ProductTransformer
from transformers.csv_transformer import CsvTransformer


class TranformerFactory:

    @staticmethod
    def get_transformer(feed_type):
        if feed_type == "PRODUCT":
            return ProductTransformer()
        if feed_type == "CSV":
            return CsvTransformer()

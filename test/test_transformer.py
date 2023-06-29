from utils.transformer.base_transformer import BaseTransformer


class TestTransformer(BaseTransformer):
    
    # add specified transformations to the given chunk
    def add_transformations(self, data: object, **kwargs) -> object:
        ''' Add required transformations here '''
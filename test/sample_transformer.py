from utils.transformer.base_transformer import BaseTransformer


class SampleTransformer(BaseTransformer):
    
    # add specified transformations to the given chunk
    def add_transformations(self, data: object, **kwargs) -> str:
        ''' Add required transformations here '''
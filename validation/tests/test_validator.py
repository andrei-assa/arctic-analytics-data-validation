from unittest import TestCase
from validation.validator import DataValidator
from validation.transformer import DataTransformer

data_transformer = DataTransformer("validation/data/order_products_prior_subset.csv")


class Test(TestCase):
    def test_data_validator(self):
        transformed_data = data_transformer.transform()
        import pdb; pdb.set_trace()
        validator = DataValidator(data=transformed_data)
        print(validator.is_valid)

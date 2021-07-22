from unittest import TestCase
from ..validator import DataValidator
from ..transformer import DataTransformer

data_transformer = DataTransformer("data/order_products_prior_subset.csv")


class Test(TestCase):
    def test_data_validator(self):
        transformed_data = data_transformer.transform()
        validator = DataValidator(data=transformed_data)
        print(validator.is_valid)
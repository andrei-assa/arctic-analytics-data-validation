from transformer import DataTransformer
from validator import DataValidator

data_transformer = DataTransformer(filepath="data/order_products_prior_subset.csv", nrows=1000000)
transformed_data = data_transformer.transform()


data_validator = DataValidator()
data_validator.validate(transformed_data)
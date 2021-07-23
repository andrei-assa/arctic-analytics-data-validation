"""
Runs tests on DataTransformer and DataValidator Class.
"""

import os
import pandas as pd
from transformer import DataTransformer
from validator import DataValidator


if __name__ == "__main__":
    # Set data directory
    data_dir = "data" if "data" in os.listdir() else "../data"
    filename = "order_products_prior_subset.csv"
    filepath = f"{data_dir}/{filename}"

    data_transformer = DataTransformer(filepath)

    transformed_data = data_transformer.transform()
    non_transformed_data = data_transformer.data.copy()

    invalid_data = pd.DataFrame()
    invalid_data["order_id"] = [1, 2, 3]
    # Invalid because data contains tuples instead of lists
    invalid_data["product_id"] = [("one", "two"), ("three", "four"), ("five", "six")]

    for name, value in [("long", non_transformed_data), ("short", transformed_data), ("invalid", invalid_data)]:
        data_validator = DataValidator(data=value)
        result = data_validator.validate_format()
        print(f"format={name}", f"valid-result={result}")

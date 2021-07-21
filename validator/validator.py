"""
Defines DataValidator class.
"""

from pandas import DataFrame
from typing import Optional

"""
    Requirements:
    1. Should identify whether data is in one-row-per-product or one-row-per-order format.
    2. If one-row-per-order, ensures that order ids are unique
    3. If one-row-per-product, transforms the data to one-row-per-order
    4. ... come up with additional validation rules here.
    
    Long-Format Data (one-row-per-product)
    ----------------
    1. Non-unique order ids
    2. Product ids are builtins (int, str)
    
    
    Short-Format Data (one-row-per-order)
    ----------------
    1. Unique order ids
    2. Product ids in list[int, str]
    
    
    Data is either:
        long format
        short format
        some other invalid format

"""


# Defines custom-defined data validation Exceptions
class NonUniqueValueError(Exception):
    """Exception raised when data values in column should be, but are not unique."""
    def __init__(self, column_name, message="Values in the column should be unique."):
        self.column_name = column_name
        self.message = message
        super().__init__(self.message)


class NonNullError(Exception):
    """Excaption raised when a value is missing, but it should be NON-NULL."""
    def __init__(self, column_name, message="Some value in the column is null. Please fill in missing values."):
        self.column_name = column_name
        self.message = message
        super().__init__(self.message)


class DataTypeException(Exception):
    """Exception raised when data type is incorrect."""
    def __init__(self, column_name, data, message="Data type is incorrect. Please check that all data has correct type."):
        self.column_name = column_name
        self.data = data
        self.message = message        
        super().__init__(self.message)


class FieldNotExistsError(Exception):
    def __init__(self, field_name):
        message = "The field name '%s' does not exist in the data" % field_name
        super().__init__(message)


class DataValidator(object):

    def __init__(self, *, data: DataFrame, order_id_col_name: Optional[str] = None, product_id_col_name: Optional[str] = None):
        self.data = data
        self._order_id_col_name = "order_id" if order_id_col_name is None else order_id_col_name
        self._product_id_col_name = "product_id" if product_id_col_name is None else product_id_col_name

        for field in self._order_id_col_name, self._product_id_col_name:
            if field not in self.data.columns:
                raise FieldNotExistsError(field_name=field)


    def validate_format(self):
        """
        Purpose: Identifies whether data is one-row-per-product or one-row-per-order format.
        Returns True when data is either of the two identified formats, otherwise returns False.

        Note: We don't assume product_ids and order_ids are integers.
        """
        
        # By default, data is neither long nor short format.
        self._long_format = False 
        self._short_format = False


        def _check_list_like(value):
            if isinstance(value, list): 
                # Regular list type: [1,2,3]
                return True

            elif isinstance(value, str) and value.strip()[0] == '[' and value.strip()[-1] == ']': 
                # String type that represents a list: '[1,2,3]', ' [1,2,3]'
                return True

            else: # Not list-like.
                return False

        order_ids_unique = self.data[self._order_id_col_name].is_unique

        product_ids_as_lists = list(self.data[self._product_id_col_name].apply(_check_list_like))
        all_product_ids_are_lists = all(product_ids_as_lists)

        # Short format data: (1) unique order id's, (2) product id's in list[(int, str)]
        if order_ids_unique and all_product_ids_are_lists:
            self._short_format = True

        # Long format data: (1) non-unique order id's
        elif not order_ids_unique:
            self._long_format = True

        else:
            print("Data is of unknown format. Please check your inputs.")

        return self._long_format or self._short_format


    def validate_data_type(self):
        """
        Purpose: Checks that all input data in 'product id' and 'order id' columns are correct data type.

        """
        # Check that order id's are of correct data type (int, str).
        order_ids_correct_data_type = all([isinstance(x, (int, str)) for x in self.data[self.order_id_col_name]])

        # Check that product id's are of correct data type (int, str).
        product_ids_correct_data_type = all([isinstance(x, (int, str)) for x in self.data[self.product_id_col_name]])

        if not order_ids_correct_data_type:
            raise DataTypeException(self.order_id_col_name)
            
        elif not product_ids_correct_data_type:
            raise DataTypeException(self.product_id_col_name)

        return order_ids_correct_data_type and product_ids_correct_data_type

    # TODO: If self._long_format, transform data to self._long_format here.


if __name__ == '__main__':
    # TODO: May move this to test_file / test dir.
    import os
    import pandas as pd
    from transformer import DataTransformer

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
        result = data_validator.validate()
        print(f"format={name}", f"valid-result={result}")

"""
Defines DataValidator class.
"""

# Requirements:
# 1. Should identify whether data is in one-row-per-product or one-row-per-order format.
# 2. If one-row-per-order, ensures that order ids are unique
# 3. If one-row-per-product, transforms the data to one-row-per-order
# 4. ... come up with additional validation rules here.

# Defines custom-defined data validation Exceptions
class NonUniqueValueError(Exception):
    """Exception raised when data values in column should be, but are not unique."""
    def __init__(self, column_name, message="Values in the column should be unique."):
        self.column_name = column_name
        self.message = message
        super().__init__(self.message)

class NonNullError(Exception):
    """Excaption raised when data value is missing, but it should be not null."""
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


class DataValidator(object):

    def __init__(self, order_id_col_name=None, product_id_col_name=None):
        self._order_id_col_name = "order_id" if order_id_col_name is None else order_id_col_name
        self._product_id_col_name = "product_id" if product_id_col_name is None else product_id_col_name
        self._data_format = None


    def validate(self, transformed_data):
        # identify whether data is one-row-per-product or one-row-per-order format
        if isinstance(transformed_data["product_id"][0], int): # if True, is one-row-per-product format
            self._data_format = 0

        elif isinstance(transformed_data["order_id"][0], int): # if True, is one-row-per-order format
            self._data_format = 1
        
        
        if self._data_format: # If data is one-row-per-order format:
            
            # Check that each order id is UNIQUE. O(n)
            if list(transformed_data["order_id"]) != set(transformed_data["order_id"]): 
                raise NonUniqueValueError("order_id") 

            # Check that each order id is correct data type (INTEGER).
            if not all([isinstance(x, int) for x in transformed_data["order_id"]]):
                raise DataTypeException(column_name="order_id", data=x)
            # Check that each product id is correct data type (INTEGER).
            if not all([isinstance(x, int) for y in transformed_data["product_id"]] for x in y):
                raise DataTypeException(column_name="product_id", data=x)

            # Check that all orders are matched with at least one product. Otherwise, there exists a NULL field.
            for x in transformed_data["product_id"]:
                if x == []:
                    raise NonNullError("product_id")


        if not self._data_format: # If data is one-row-per-product format:
    
            # Check that each product id is UNIQUE. O(n)
            if list(transformed_data["product_id"]) != set(transformed_data["product_id"]): 
                raise NonUniqueValueError("product_id")

            # Check that each product id is correct data type (INTEGER).
            if not all([isinstance(x, int) for x in transformed_data["product_id"]]):
                raise DataTypeException(column_name="product_id", data=x)
            # Check that each order id is correct data type (INTEGER).
            if not all([isinstance(x, int) for y in transformed_data["order_id"]] for x in y):
                raise DataTypeException(column_name="order_id", data=x)

            # Check that all products are matched with at least one order. Otherwise, there exists a NULL field.
            for x in transformed_data["order_id"]:
                if x == []:
                    raise NonNullError("order_id")

        # TODO: Check other columns are also of correct data type.
        # TODO: Check MIN and MAX values?


if __name__ == '__main__':
    data_validator = DataValidator()
    data_validator.validate(transformed_data) # validates data that was transformed from `transformer.py`
"""
Defines DataValidator class.
"""

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
        # Don't assume product_ids and order_ids are integers
        
        """
        if one-row-per-order:
            
        """
        
        self._order_ids_unique = False
        self._product_ids_are_list = False
        self._product_ids_are_str_or_int = False
        self._product_ids_in_list_are_int_strings = False
        
        # if self._order_ids_unique and self._product_ids_are_list:
            # self._short_format = True
        # elif not self._order_ids_unique (and self._order_ids_str_or_int) and self._product_ids_are_str_or_int:
            # self._long_format = True

        
        self._long_format = False
        self._short_format = False
        
        if not isinstance(transformed_data["order_id"][0], list): # if True, is one-row-per-product format (long-format)
            self._long_format = True

        elif not isinstance(transformed_data["product_id"][0], list): # if True, is one-row-per-order format (short-format)
            self._short_format = True
        else:
            raise RuntimeError


        # TODO: serialize all columns astype(str), put the following two lines there:
        transformed_data["order_id"] = transformed_data["order_id"].astype(str)
        transformed_data["product_id"] = transformed_data["product_id"].astype(str)


        if self._short_format: # If data is one-row-per-order (short format):
            
            # Check that each order id is UNIQUE. O(n)
            if len(transformed_data) != len(set(transformed_data["order_id"])): 
                raise NonUniqueValueError("order_id")

            # Check that each order id is correct data type (INTEGER).
            if not all([isinstance(x, int) for x in transformed_data["order_id"]]):
                raise DataTypeException(column_name="order_id", data=x)
            # Check that each product id is correct data type (INTEGER).
            if not all([isinstance(x, int) for y in transformed_data["product_id"]] for x in y):
                raise DataTypeException(column_name="product_id", data=x)

            # Check that all orders are matched with at least one product. Otherwise, there exists a NULL field.
            for x in transformed_data["product_id"]:
                if not x:
                    raise NonNullError("product_id")


        if not self._long_format: # If data is one-row-per-product (long format):
            
            # Check that each product id is UNIQUE. O(n)
            if len(list(transformed_data["product_id"])) != len(set(transformed_data["product_id"])): 
                raise NonUniqueValueError("product_id")

            # Check that each product id is correct data type (INTEGER).
            if not all([isinstance(x, int) for x in transformed_data["product_id"]]):
                raise DataTypeException(column_name="product_id", data=x)
            # Check that each order id is correct data type (INTEGER).
            if not all([isinstance(x, int) for y in transformed_data["order_id"]] for x in y):
                raise DataTypeException(column_name="order_id", data=x)
            
            """
                order_id    product_id
                1           []
            """

            # Check that all products are matched with at least one order. Otherwise, there exists a NULL field.
            for x in transformed_data["order_id"]:
                if not x:
                    raise NonNullError("order_id")

        # TODO: Check other columns are also of correct data type.
        # TODO: Check MIN and MAX values?


if __name__ == '__main__':
    data_validator = DataValidator()
    data_validator.validate(transformed_data) # validates data that was transformed from `transformer.py`
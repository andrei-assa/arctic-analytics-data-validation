"""
Defines DataValidator class.
"""

# Requirements:
# 1. Should identify whether data is in one-row-per-product or one-row-per-order format.
# 2. If one-row-per-order, ensures that order ids are unique
# 3. If one-row-per-product, transforms the data to one-row-per-order
# 4. ... come up with additional validation rules here.

class DataValidator(object):

    def __init__(self, order_id_col_name=None, product_id_col_name=None):
        self._order_id_col_name = "order_id" if order_id_col_name is None else order_id_col_name
        self._product_id_col_name = "product_id" if product_id_col_name is None else product_id_col_name

        pass

    def validate(self):
        pass


if __name__ == '__main__':
    data_validator = DataValidator()
    data_validator.validate()
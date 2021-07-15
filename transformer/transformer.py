"""
DataTransformer class.
"""

import pandas as pd

class DataTransformer(object):

    def __init__(self, filepath: str, verbose: bool = False) -> None:
        """

        Args:
            filepath (str): Path to file.
            verbose (bool): Verbose output.
        """
        self._filepath = filepath
        self._data = self._load_data()
        self.data = self._data.copy()
        self._verbose = verbose
        self._transformed_data = None


    def _load_data(self):
        return pd.read_csv(self._filepath)

    def reset(self):
        self.data = self._data.copy()
        self._transformed_data = None
        if self._verbose:
            print("Data has been reset")

    def transform(self):
        """Transform data from one-row-per-product to one-row-per-order.

        Returns:
            pandas.DataFrame: Transformed data.

        """
        # TODO: As implemented, runs in O(n) time, re-implement to use array broadcasting.

        if self._transformed_data is None:

            output_dict = {}
            order_id_tuple = tuple(self.data.order_id.unique())
            for order_id in order_id_tuple:
                data_subset = self.data[self.data.order_id == order_id]
                product_id_list = list(data_subset.product_id)
                output_dict[order_id] = str(product_id_list)
            output = pd.DataFrame().from_dict(output_dict, orient="index")
            output = output.rename({0:"product_id"}, axis=1)
            output = output.reset_index()
            output = output.rename({"index": "order_id"}, axis=1)

            # Cache the data so it does not have to be transformed de-novo each time.
            self._transformed_data = output

        return self._transformed_data


if __name__ == '__main__':
    data_transformer = DataTransformer(filepath="data/order_products__prior.csv")
    transformed_data = data_transformer.transform()

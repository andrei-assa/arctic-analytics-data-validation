"""
DataTransformer class.
"""

import pandas as pd

class DataTransformer(object):

    def __init__(self, filepath: str, nrows: int = 100000, verbose: bool = False) -> None:
        """

        Args:
            filepath (str): Path to file.
            verbose (bool): Verbose output.
        """
        self._filepath = filepath
        self._data = self._load_data(nrows=nrows)
        self.data = self._data.copy()
        self._verbose = verbose
        self._transformed_data = None


    def _load_data(self, nrows):
        return pd.read_csv(self._filepath, nrows=nrows)

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

        def _transform(x):
            result = list(x.values)
            result.sort()
            return result


        if self._transformed_data is None:
            grouped = self.data.groupby("order_id")
            result = grouped.agg(_transform)
            result = result.reset_index()
            self._transformed_data = result

        return self._transformed_data


if __name__ == '__main__':
    data_transformer = DataTransformer(filepath="data/order_products_prior_subset.csv")
    transformed_data = data_transformer.transform()

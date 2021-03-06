"""
DataTransformer class.
"""

import pandas as pd


class DataTransformer(object):
    def __init__(
        self,
        *,
        data: pd.DataFrame = None,
        filepath: str = None,
        nrows: int = 100000,
        verbose: bool = False
    ) -> None:

        self._filepath = filepath
        self._data = data

        if self._filepath is None and self._data is None:
            raise RuntimeError("Must supply either filepath or data")
        elif self._data is not None and self._filepath is not None:
            raise RuntimeError("Must supply only filepath or data, not both")
        elif self._data is not None:
            pass
        else:
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
        def _transform_to_list(x):
            data_list = list(x.values)
            data_list.sort()
            return data_list

        if self._transformed_data is None:
            grouped = self.data.groupby("order_id")
            result = grouped.agg(_transform_to_list)
            result = result.reset_index()
            self._transformed_data = result

        return self._transformed_data


if __name__ == "__main__":
    data_transformer = DataTransformer(
        filepath="data/order_products_prior_subset.csv"
    )
    transformed_data = data_transformer.transform()

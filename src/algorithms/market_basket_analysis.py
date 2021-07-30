"""Example of market basket analysis."""

import pandas as pd
import sys
from mlxtend.frequent_patterns import apriori, association_rules
from src.utils.utils import get_project_root

project_root = get_project_root()
sys.path.insert(0, project_root)
from validation.transformer import DataTransformer

data_directory = f"{project_root}/data"
orders_fp = "order_products_prior_subset.csv"
products_fp = "products.csv"

orders = pd.read_csv(f"{data_directory}/{orders_fp}")
products = pd.read_csv(f"{data_directory}/{products_fp}")

orders = orders.merge(products, on="product_id", how="left")
baking_supplies = orders[orders.department_id==10]
baking_supplies_order_ids = list(baking_supplies.order_id.unique())
subset = orders[orders.order_id.isin(baking_supplies_order_ids)]
subset = subset[["order_id", "product_name"]]

transformer = DataTransformer(data=subset)

raise KeyboardInterrupt

subset = subset.set_index(["order_id", "product_name"])
subset["orders"] = 1
subset = subset.unstack().fillna(0)
col_names = [x[1] for x in subset.columns]
subset.columns = col_names

# baking_supplies.unstack()
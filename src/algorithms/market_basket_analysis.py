"""Example of market basket analysis."""

import pandas as pd
import sys
from mlxtend.frequent_patterns import apriori, association_rules
from src.utils.utils import get_project_root

project_root = get_project_root()

data_directory = f"{project_root}/data"
orders_fp = "order_products_prior_subset.csv"
products_fp = "products.csv"

orders = pd.read_csv(f"{data_directory}/{orders_fp}")
products = pd.read_csv(f"{data_directory}/{products_fp}")

orders = orders.merge(products, on="product_id", how="left")
subset = orders[orders.department_id ==5]
subset = subset[["order_id", "product_name"]]
subset["ordered"] = 1

basket = subset.groupby(['order_id', 'product_name'])["ordered"]
basket_matrix = basket.sum().unstack().reset_index().fillna(0).set_index('order_id')
itemsets = apriori(basket_matrix, min_support=0.001, use_colnames=True)
rules = association_rules(itemsets)

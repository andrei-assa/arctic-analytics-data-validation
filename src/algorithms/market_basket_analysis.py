"""Example of market basket analysis."""

import sys
import pandas as pd
import argparse
from pathlib import Path
import numpy as np
this_file = Path(__file__)
project_root = str(this_file.parent.parent.absolute())
sys.path.insert(0, project_root)

from mlxtend.frequent_patterns import apriori, association_rules
from utils.utils import get_project_root

parser = argparse.ArgumentParser("An argument parser for market basket analysis")

parser.add_argument("--department", help="Select department")
parser.add_argument("--debug", help="Enter debug mode")
parser.add_argument("--min-support", help="Minimum support value")
parser.add_argument("--min-results", help="Minimum number of rules to generate")
args = parser.parse_args()

SLEEP = 0 

DEPARTMENT_ID = int(args.department if args.department is not None else 5)
MIN_SUPPORT = float(args.min_support if args.min_support is not None else 0.01)
DEBUG_MODE = bool(args.debug)
MIN_RESULTS = int(args.min_results) if args.min_results is not None else 0

data_directory = f"{project_root}/data"
orders_fp = "order_products_prior_subset.csv"
products_fp = "products.csv"

orders = pd.read_csv(f"{data_directory}/{orders_fp}")
products = pd.read_csv(f"{data_directory}/{products_fp}")

orders = orders.merge(products, on="product_id", how="left")
subset = orders[orders.department_id == DEPARTMENT_ID ]
subset = subset[["order_id", "product_name"]]
subset["ordered"] = 1

basket = subset.groupby(['order_id', 'product_name'])["ordered"]
basket_matrix = basket.sum().unstack().reset_index().fillna(0).set_index('order_id')
apriori_results = pd.DataFrame()
rules = pd.DataFrame()

increment_upward = False

if DEBUG_MODE:
    import pdb; pdb.set_trace()

from time import sleep

last_success_min_support = float("inf")
success = False
last_min_support = None
# while we have not generated any results yet...
while rules.empty or len(rules) < MIN_RESULTS:
    sleep(SLEEP)
    # round the MIN_SUPPORT value to 10 decimal places
    MIN_SUPPORT = round(MIN_SUPPORT, 10)
    # if min_support has been incrementing upward and has reached the last min_support success value without
    # encountering success, break out of the loop
    if MIN_SUPPORT >= last_success_min_support:
        if (not success) or (MIN_SUPPORT == last_min_support):
            print(f"No rules able to be created with specified settings")
        else:
            print(f"Created {len(rules)} rules from the specified settings.")
        break

    # check if we are currently on some fraction of 10
    is_decimal_of_10 = int(np.log10(MIN_SUPPORT)) == np.log10(MIN_SUPPORT)
    
    if is_decimal_of_10 and not increment_upward:
        # if we are currently on some decimal of 10, set a new decrement
        DECREMENT = MIN_SUPPORT / 10
        print(f"{MIN_SUPPORT} is a decimal of 10")
    
    if MIN_SUPPORT == last_min_support:
        print("breaking out of loop")
        break

    try:    
        last_min_support = MIN_SUPPORT
        print(f"Attempting to create association rules with min_support = {MIN_SUPPORT}") 
        apriori_result = apriori(basket_matrix, min_support=MIN_SUPPORT, use_colnames=True)
        rules = association_rules(apriori_result)
        # if either of these fails due to memory issues, go to except block
        # if rules is empty, go to the start
        if apriori_results.empty or rules.empty:
            if not increment_upward:
                MIN_SUPPORT -= DECREMENT
            continue
        
        elif not rules.empty:
            # if rules is not empty, we were successful; but were enough rules generated?
            print(f"Success at {MIN_SUPPORT}")
            last_success_min_support = MIN_SUPPORT
            success = True
            print(f"Last success at {last_success_min_support}")
    
    except Exception as e:
        # apriori_result or rules were not generated due to memory constrainsts; increase the MIN_SUPPORT
        error = e
        MIN_SUPPORT += DECREMENT / 10
        print(f"Encountered error: {error}: incrementing upward to {MIN_SUPPORT}")
        increment_upward = True
        continue

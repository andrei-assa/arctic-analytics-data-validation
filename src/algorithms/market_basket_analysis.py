"""Example of market basket analysis."""

# Importing depdencies
import sys
import pandas as pd
import argparse
from pathlib import Path
import numpy as np
from time import sleep
this_file = Path(__file__)
project_root = str(this_file.parent.parent.absolute())
sys.path.insert(0, project_root)

from mlxtend.frequent_patterns import apriori, association_rules

# Getting arguments from the command line
parser = argparse.ArgumentParser("An argument parser for market basket analysis")
parser.add_argument("--department", help="Select department")
parser.add_argument("--debug", help="Enter debug mode")
parser.add_argument("--min-support", help="Minimum support value")
parser.add_argument("--min-results", help="Minimum number of rules to generate")
args = parser.parse_args()

# If we want to slow the rate of iterations through the program for debugging.
SLEEP = 0

# These are the variables from the command line; we are setting some default values
# if nothing is passed from the command line.
DEPARTMENT_ID = int(args.department if args.department is not None else 5)
MIN_SUPPORT = float(args.min_support if args.min_support is not None else 0.01)
DEBUG_MODE = bool(args.debug) #If we want to enter the debugger; use pdb.set_trace()
MIN_RESULTS = int(args.min_results) if args.min_results is not None else 0
MAX_ATTEMPTS = 11

# Defining the directory paths to the data.

data_directory = f"{project_root}/data"
orders_fp = "order_products_prior_subset.csv"
products_fp = "products.csv"

# Getting the orders and products dataframes.
orders = pd.read_csv(f"{data_directory}/{orders_fp}")
products = pd.read_csv(f"{data_directory}/{products_fp}")

# Merging the orders and products dataframes on product_id column.
orders = orders.merge(products, on="product_id", how="left")

# Getting a one-department subset from the orders dataframe based on
# whichever department was passed in from the command line.
# FROM HERE DOWARD, WE ARE FILTERING DATA DEPARTMENT_SUBSET BY DEPARTMENT_ID
DEPARTMENT_SUBSET = orders[orders.department_id == DEPARTMENT_ID ]
DEPARTMENT_SUBSET = DEPARTMENT_SUBSET[["order_id", "product_name"]]
DEPARTMENT_SUBSET["ordered"] = 1


# Creating the basket_matrix from DEPARTMENT_SUBSET
basket = DEPARTMENT_SUBSET.groupby(['order_id', 'product_name'])["ordered"]
basket_matrix = basket.sum().unstack().reset_index().fillna(0).set_index('order_id')

# These print statements are useful for basket size.
print(f"DEPARTMENT_ID=", DEPARTMENT_ID)
print("basket_matrix.size=", basket_matrix.size)

# We are generating empty dataframes:
# We are using these dataframes to generate a condition in the while loop below.
# Empty dataframes
apriori_results = pd.DataFrame()
rules = pd.DataFrame()


# If we specified debug mode in command line, enter here.
if DEBUG_MODE:
    import pdb; pdb.set_trace()


# last_success_min_support = float("inf")
# success = False
# last_min_support = None

# while we have not generated any results yet...
# Find the value of MIN_SUPPORT that is just large enough to NOT throw a memory error
    # MAX. size of market_basket_matrix: 199557120, Department ID: 19

# We started with an empty rules dataframe, we are going to keep checking if it is empty
count = 0
while rules.empty or len(rules) < MIN_RESULTS:
    count += 1
    if count > MAX_ATTEMPTS:
        print("Reached max_attempts")
        raise KeyboardInterrupt
    else:
        print(f"Attempt #{count}")
    
    # If we are sleeping i.e. slowing down the program, do that now.
    sleep(SLEEP)
    
    # round the MIN_SUPPORT value to 10 decimal places
    # if starting at 0.01 --> 0.009 --> 0.008 --> 
    # start 0.01 --> 0.001 --> if empty --> 0.0001
    #                0.001 --> memory error --> 0.005
    # 10e-10 --> end
    # The SMALLEST possible value of MIN_SUPPORT 0.0000000001

    MIN_SUPPORT = round(MIN_SUPPORT, 10)
    MIN_SUPPORT /= 10
    # if min_support has been incrementing upward and has reached the last min_support success value without
    # encountering success, break out of the loop

    # if MIN_SUPPORT >= last_success_min_support:
    #     if (not success) or (MIN_SUPPORT == last_min_support):
    #         print(f"No rules able to be created with specified settings")
    #     else:
    #         print(f"Created {len(rules)} rules from the specified settings.")
    #     break

    # check if we are currently on some fraction of 10
    # is_decimal_of_10 = int(np.log10(MIN_SUPPORT)) == np.log10(MIN_SUPPORT)
    
    
    #     # if we are currently on some decimal of 10, set a new decrement
    #     print(f"{MIN_SUPPORT} is a decimal of 10")
    
    # if MIN_SUPPORT == last_min_support:
    #     print("breaking out of loop")
    #     break

    try:    
        last_min_support = MIN_SUPPORT
        print(f"Attempting to create association rules with min_support = {MIN_SUPPORT}")

        # Two main dataframes of while loop
        # APRIORI_RESULT must be filtered for baskets that only contain single items. 
        apriori_result = apriori(basket_matrix, min_support=MIN_SUPPORT, use_colnames=True)
        # TODO: filter out rules where only single item
        # apriori_result = apriori_results[apriori_result.itemsets > 1]
        rules = association_rules(apriori_result)


        # if either of these fails due to memory issues, go to except block
        # if rules is empty, go to the start
        if apriori_results.empty or rules.empty:
                
                MIN_SUPPORT /= 10 
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

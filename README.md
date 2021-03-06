# Arctic Analytics 

- [Arctic Analytics](#arctic-analytics)
  - [Project Structure](#project-structure)
  - [Algorithms](#algorithms)
    - [Market Basket Analysis](#market-basket-analysis)
  - [Notes from 7/30 Meeting](#notes-from-730-meeting)

## Project Structure

```tree
.
├── README.md
├── pyvenv.cfg
├── requirements.txt
└── src
    ├── algorithms
    │   ├── __init__.py
    │   └── market_basket_analysis.py
    ├── data
    │   ├── instacart_data_subset.zip
    │   ├── order_products_prior_subset.csv
    │   ├── products.csv
    │   └── products.csv.zip
    ├── streamlit_app
    │   ├── app.py
    │   ├── data.db
    │   ├── test1.csv
    │   ├── test1.py
    │   └── uber_pickups.py
    └── validation
        ├── __init__.py
        ├── tests
        │   ├── __init__.py
        │   ├── test_transformer.py
        │   └── test_validator.py
        ├── transformer
        │   ├── __init__.py
        │   └── transformer.py
        └── validator
            ├── __init__.py
            └── validator.py
```

## Algorithms

### Market Basket Analysis

![Image](images/mermaid-diagram-20210802162612.png)

## Notes from 7/30 Meeting

- Task 1: multiple tables in excel doc -> return Err: ask user to reformat data  
- Task 2: Tutorial? Sample data/ columns guideline  
- Task 3: Basic cleaning data (e.g. null values etc)  
- Task 4: Filtering dataset?  

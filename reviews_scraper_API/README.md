## Run instructions

Install dependencies:

The `selectorlib` module can be installed by running:
```
pip install selectorlib
```


Run the following command:
```
flask run 
```


## Tailoring tool to target website

1. Go to target website url
2. Using selectorlib, select pattern of elements you wish to scrape -> compile into .yml file 
(Check out: https://selectorlib.com/ for documentation on how to do this)
3. Run flask API, then navigate to https://localhost:5000
4. Paste target website url, then submit.

Note: Check out the following files for examples: *etsy_selectors.yml*, *target_selectors.yml*, *amazon_selectors.yml* 

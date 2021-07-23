import json, falcon
import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# import pdb; pdb.set_trace()

from validation.validator import DataValidator


"""
Purpose: Simple server for Apriori REST API in Python, based on Falcon.

To test requests using Postman, go to : 
https://grey-escape-108703.postman.co/workspace/2fb62228-e692-4092-b642-f64d2956fca2/request/16724741-e816737e-3bbe-4893-bd4f-5206ced10a33

"""

class ObjRequestClass:
    def on_get(self, req, res):
        """
        Purpose: Makes a simple GET request to our REST API, WITHOUT body.
        """
        """
        import os
        import pandas as pd
        from transformer import DataTransformer
        import json

        data_as_json = json.loads(req.data)

        # dir(req) / req.__dict__ req.data <--


        data = pd.DataFrame(data_as_json)

        # Set data directory
        data_dir = "data" if "data" in os.listdir() else "../data"
        filename = "order_products_prior_subset.csv"
        filepath = f"{data_dir}/{filename}"

        data_transformer = DataTransformer(filepath)
        non_transformed_data = data_transformer.data.copy()

        invalid_data = pd.DataFrame()
        invalid_data["order_id"] = [1, 2, 3]

        # Invalid because data contains tuples instead of lists
        invalid_data["product_id"] = [("one", "two"), ("three", "four"), ("five", "six")]
        

        for name, value in [("long", non_transformed_data), ("invalid", invalid_data)]:
            data_validator = DataValidator(data=value)
            result = data_validator.is_valid
            print(f"format={name}", f"valid-result={result}")
        """

        
        # examine req

        content = { # replace with appropriate content for Apriori algorithm.
            'name': 'Jon',
            'age': '30',
            'country': 'New Caledonia'
        }

        res.body = json.dumps(content)
        print("GET request on our falcon API")


    """ Uncomment to switch to slightly more complex sample:
    Purpose: Makes a GET request to our REST API, WITH body.

    def on_get(self, req, res): 
        data = json.loads(req.stream.read())
        print(data)
         
        content = {
            'name': 'Jon',
            'age': '30',
            'country': 'New Caledonia'
        }

        output = {}
        if data["name"]:
            output["value"] = content["country"]
        else:
            output["value"] = "Hello user"
        
        res.body = json.dumps(output)
    """


    def on_post(self, req, res):
        """
        Purpose: Makes a POST request to our REST API, WITH body.
        """
        output = ""

        
        try:
            json_string = req.stream.read()
        except:
            output = "Could not read stream"

        try:
            python_dictionary = json.loads(json_string)

            try:
                pandas_dataframe = pd.DataFrame(
                    python_dictionary,
                    # index=index
                )
                print(pandas_dataframe)
                validator = DataValidator(data=pandas_dataframe)
                output = validator.is_valid

            except:
                output = "Data could not be loaded correctly"

        except: #TODO: Make expcetion more specific
            output = "Could not parse JSON"

        print("result :", output)
        
        message = {
            'msg' : 'Message: {0}'.format(output)
        }

        # JSON could not be loaded
        # pandas DataFrame could not be loaded
        # pandas DataFrame was loaded, but data invalid
        # pandas DataFrame loaded and data valid

        # res.body = json.dumps({"response":validator.is_valid})
        res.body  = json.dumps(message)


api = falcon.API()
api.add_route('/test', ObjRequestClass())

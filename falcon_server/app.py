import json, falcon

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
        content = { # replace with appropriate content for Apriori algorithm.
            'name': 'Jon',
            'age': '30',
            'country': 'New Caledonia'
        }

        res.body = json.dumps(output)
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
        data = json.loads(req.stream.read())

        result = int(data['x']) + int(data['y']) # Replace with Apriori algorithm.

        output = {
            'msg' : 'x: {0} + y: {1} is equals {2}'.format(data['x'], data['y'], result)
        }
    
        res.body  = json.dumps(output)


api = falcon.API()
api.add_route('/test', ObjRequestClass())

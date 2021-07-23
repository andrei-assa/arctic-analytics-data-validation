"""
Purpose: Simple server for Apriori REST API in Python, based on Falcon.

To test requests using Postman, go to :
https://grey-escape-108703.postman.co/workspace/2fb62228-e692-4092-b642-f64d2956fca2/request/16724741-e816737e-3bbe-4893-bd4f-5206ced10a33

"""
import json
import falcon
import pandas as pd
from validation.validator import DataValidator


# Don't rename ObjRequestClass methods, falcon expects these methods as part of API.

class ObjRequestClass:
    # TODO: Enter description.

    def on_get(
        self, req: falcon.request.Request, res: falcon.response.Response
    ) -> falcon.response.Response:
        """

        Args:
            req ():
            res ():

        Returns:

        """
        try:
            content = req.stream.read()
            res.body = json.dumps(content)
            print("GET request on our falcon API")
        except:
            raise Exception
        raise NotImplementedError


    def on_post(
        self,
        req: falcon.request.Request,
        res: falcon.response.Response
    ) -> falcon.response.Response:
        """

        Args:
            req ():
            res ():

        Returns:

        """
        output = None

        try:

            json_string = req.stream.read().decode()
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
                except:  # TODO: Make exception more specific
                    output = "Data could not be loaded correctly"
            except:  # TODO: Make expcetion more specific
                output = "Could not parse JSON"
        except:  # TODO: Make expcetion more specific
            output = "Could not read stream"
        print("result :", output)

        message = {"msg": "Message: {0}".format(output)}

        res.body = json.dumps(message)
        # return res


api = falcon.API()
api.add_route("/test", ObjRequestClass())

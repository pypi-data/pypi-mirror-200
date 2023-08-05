import requests
from customate.api_resources.mixins import dict_json_convertor

class APIRequestor:

    def __init__(self, **kwargs):

        self.method = kwargs.get("method")
        self.url = kwargs.get("url")
        self.headers = kwargs.get("headers")
        self.data = kwargs.get("data")

    def post(self):
        response = requests.post(
                self.url,
                headers=self.headers,
                data=dict_json_convertor(self.data)
            )
        return response
    
    def put(self):
        response = requests.put(
                self.url,
                headers=self.headers,
                data=dict_json_convertor(self.data)
            )
        return response
    
    def get(self):
        response = requests.get(
                self.url,
                headers=self.headers,
            )
        return response

    def delete(self):
        response = requests.delete(
                self.url,
                headers=self.headers,
            )
        return response
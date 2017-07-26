import requests

BASE_URL = 'https://api.upcitemdb.com/prod/trial'


class UPCItemDBClient:
    def __init__(self):
        pass

    def lookup(self, upc):
        url = '/lookup'
        params = {'upc': upc}
        response = requests.get(BASE_URL + url, params=params)
        return response.json()
        

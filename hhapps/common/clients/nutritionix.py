# main code from https://github.com/nutritionix/library-python

import logging
import requests
import urllib.parse

API_VERSION = "v1_1"
BASE_URL = "https://api.nutritionix.com/%s/" % (API_VERSION)
# https://developer.nutritionix.com/docs/v1_1


class NutritionixClient:

    def __init__(self,
                 application_id=None,
                 api_key=None,
                 debug=False):
        self.APPLICATION_ID = application_id
        self.API_KEY = api_key
        self.DEBUG = False

        if debug:
            self.DEBUG = debug
            logging.basicConfig(level=logging.DEBUG)

    def get_api_version(self):
        return API_VERSION

    def get_application_id(self):
        return self.APPLICATION_ID

    def get_api_key(self):
        return self.API_KEY

    def execute(self,
                url=None,
                method='GET',
                params={},
                data={},
                headers={}):
        """ Bootstrap, execute and return request object,
                default method: GET
        """

        # Verifies params
        if params.get('limit') is not None \
                and params.get('offset') is None:
            raise Exception('Missing offset',
                            'limit and offset are required for paginiation.')

        elif params.get('offset') is not None \
                and params.get('limit') is None:
            raise Exception('Missing limit',
                            'limit and offset are required for paginiation.')

        # Bootstraps the request
        method = method.lower()

        params['appId'] = self.APPLICATION_ID
        params['appKey'] = self.API_KEY

        # Executes the request
        if method == "get" or 'method' not in locals():
            r = requests.get(url, params=params, headers=headers)

        elif method == "post":
            r = requests.post(url, params=params, data=data, headers=headers)

        else:
            return None

        # Log response content
        logging.debug("Response Content: %s" % (r.text))

        return r.json()

    def autocomplete(self, **kwargs):
        """
        Specifically designed to provide autocomplete functionality for search
        boxes. The term selected by the user in autocomplete will pass to
        the /search endpoint.
        """

        # If first arg is String then use it as query
        params = {}
        if kwargs:
            params = kwargs

        endpoint = urllib.parse.urljoin(BASE_URL, 'autocomplete')

        return self.execute(endpoint, params=params)

    def natural(self, **kwargs):
        """
        Supports natural language queries like "1 cup butter"
        or "100cal yogurt"
        """

        # If first arg is String then use it as query
        params = {}
        if kwargs:
            params = kwargs

        # Converts 'q' argument as request data
        data = ''
        if params.get('q'):
            data = params.get('q')
            # Removes 'q' argument from params to avoid pass it as URL argument
            del params['q']

        endpoint = urllib.parse.urljoin(BASE_URL, 'natural')

        return self.execute(endpoint,
                            method="POST",
                            params=params,
                            data=data,
                            headers={'Content-Type': 'text/plain'})

    def search(self, **kwargs):  # TODO: Add advance search filters
        """
        Search for an entire food term like "mcdonalds big mac" or "celery."
        """

        # Adds keyword args to the params dictionary
        params = {}
        if kwargs:
            params = kwargs

        endpoint = urllib.parse.urljoin(BASE_URL, 'search')

        return self.execute(endpoint, params=params)

    def item(self, **kwargs):
        """Look up a specific item by ID or UPC"""

        # Adds keyword args to the params dictionary
        params = {}
        if kwargs:
            params = kwargs

        endpoint = urllib.parse.urljoin(BASE_URL, 'item')

        return self.execute(endpoint, params=params)

    def brand(self, **kwargs):
        """Look up a specific brand by ID. """

        # Adds keyword args to the params dictionary
        params = {}
        if kwargs:
            params = kwargs

        endpoint = urllib.parse.urljoin(BASE_URL,
                                        'brand/%s' % (params.get('id')))

        return self.execute(endpoint)

    def brand_search(self, **kwargs):
        """Look up a specific brand by ID. """

        # Adds keyword args to the params dictionary
        params = {}
        if kwargs:
            params = kwargs

        endpoint = urllib.parse.urljoin(BASE_URL, 'search/brands/')

        return self.execute(endpoint, params=params)

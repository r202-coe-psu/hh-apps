
from flask import g, current_app

from hhapps.common.clients import nutritionix
from hhapps.common.clients import upcitemdb


def init_request_context(app):
    @app.before_request
    def init_nutritionix():
        if g.get('nutritionix', None):
            return

        config = current_app.config

        application_id = config.get('CLIENTS_NUTRITIONX_APPLICATION_ID', None)
        api_key = config.get('CLIENTS_NUTRITIONX_API_KEY', None)

        client = nutritionix.NutritionixClient(application_id=application_id,
                                               api_key=api_key)

        g.nutritionix = client

    @app.before_request
    def init_upcitemdb():
        if g.get('upcitemdb', None):
            return

        client = upcitemdb.UPCItemDBClient()
        g.upcitemdb = client

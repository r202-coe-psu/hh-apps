from flask import abort
from flask_jwt_extended import JWTManager, get_jwt_claims

from hhapps.inventory.api import models

from hhapps.common.renderers import render_json


class User:
    def __init__(self, id, roles):
        self.id = id
        self.roles = roles

def init_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_loader_callback_loader
    def user_loader_callback(identity):

        user = User(identity,
                    get_jwt_claims())
                    
        return user

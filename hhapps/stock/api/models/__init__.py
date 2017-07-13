from .common import User, Building
from .stocks import Stock

__all__ = [User, Building, Stock]

from flask_mongoengine import MongoEngine
import mongoengine as me

db = MongoEngine()


def init_db(app):
    db.init_app(app)

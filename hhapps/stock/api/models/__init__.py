from .common import User, Building
from .stocks import Stock
from .items import Item
from .inventories import Inventory

from flask_mongoengine import MongoEngine

__all__ = [User,
           Building,
           Stock,
           Item,
           Inventory]


db = MongoEngine()


def init_db(app):
    db.init_app(app)

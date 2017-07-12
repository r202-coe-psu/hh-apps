
from .inventories import Inventory, User, Building

__all__ = [User, Building, Inventory]

from flask_mongoengine import MongoEngine
import mongoengine as me

db = MongoEngine()


def init_db(app):
    db.init_app(app)

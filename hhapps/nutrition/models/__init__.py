
from .nutrition import Nutrition

__all__ =[Nutrition]

from flask_mongoengine import MongoEngine

db = MongoEngine()

def init_db(app):
    db.init_app(app)

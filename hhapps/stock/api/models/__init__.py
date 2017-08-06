from .common import User, Building
from .stocks import Stock
from .items import (Item,
                    DataSource,
                    Brand,
                    Company,
                    Allergen,
                    NutritionFact,
                    Nutrition)
from .inventories import (Inventory,
                          Consumption)

from flask_mongoengine import MongoEngine

__all__ = [User,
           Building,
           Stock,
           Item,
           DataSource,
           Brand,
           Company,
           Allergen,
           Nutrition,
           NutritionFact,
           Inventory,
           Consumption]


db = MongoEngine()


def init_db(app):
    db.init_app(app)

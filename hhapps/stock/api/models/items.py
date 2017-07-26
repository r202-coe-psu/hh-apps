import mongoengine as me
import datetime

from .common import User

CATEGORIES = ['food']


class Company(me.Document):
    name = me.StringField()
    address = me.StringField()

    created_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow)
    updated_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow,
                                    auto_now=True)

    meta = {'collection': 'companies'}


class Brand(me.Document):
    name = me.StringField()
    holder = me.ReferenceField(Company)

    created_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow)
    updated_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow,
                                    auto_now=True)

    meta = {'collection': 'brands'}


class Manufactory(me.Document):
    name = me.StringField()
    address = me.StringField()

    created_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow)
    updated_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow,
                                    auto_now=True)

    meta = {'collection': 'manufactories'}


class Allergen(me.EmbeddedDocument):
    eggs = me.BooleanField(default=False)
    fish = me.BooleanField(default=False)
    gluten = me.BooleanField(default=False)
    milk = me.BooleanField(default=False)
    peanuts = me.BooleanField(default=False)
    shellfish = me.BooleanField(default=False)
    soybeans = me.BooleanField(default=False)
    tree_nuts = me.BooleanField(default=False)
    wheat = me.BooleanField(default=False)


class NutritionFact(me.EmbeddedDocument):
    calcium_dv = me.IntField()
    calories = me.IntField()
    calories_from_fat = me.IntField()
    cholesterol = me.IntField()
    dietary_fiber = me.IntField()
    ingredient_statement = me.StringField()
    iron_dv = me.IntField()
    monounsaturated_fat = me.IntField()
    polyunsaturated_fat = me.IntField()
    protein = me.IntField()
    refuse_pct = me.IntField()
    saturated_fat = me.IntField()
    serving_size_qty = me.IntField()
    serving_size_unit = me.StringField()
    serving_weight_grams = me.IntField()
    servings_per_container = me.IntField()
    sodium = me.IntField()
    sugars = me.IntField()
    total_carbohydrate = me.IntField()
    total_fat = me.IntField()
    trans_fatty_acid = me.IntField()
    vitamin_a_dv = me.IntField()
    vitamin_c_dv = me.IntField()
    water_grams = me.IntField()


class DataSource(me.EmbeddedDocument):
    user = me.EmbeddedDocumentField(User)
    data = me.DictField()
    provider = me.StringField()

    created_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow)


class Item(me.Document):
    name = me.StringField(required=True)
    description = me.StringField()
    tags = me.ListField(me.StringField())
    upc = me.StringField(uniqued=True)
    color = me.StringField()
    size = me.StringField()
    weight = me.StringField()
    dimension = me.StringField()
    category = me.StringField(required=True,
                              choices=CATEGORIES,
                              default='food')

    brand = me.ReferenceField(Brand, dbref=True)
    manufactory = me.ReferenceField(Manufactory, dbref=True)

    sources = me.EmbeddedDocumentListField(DataSource)

    status = me.StringField(required=True, default='deactivate')

    created_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow)
    updated_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow,
                                    auto_now=True)

    meta = {'collection': 'items'}


class Nutrition(me.Document):
    item = me.ReferenceField(Item, dbref=True)
    allergen = me.EmbeddedDocumentField(Allergen)
    facts = me.EmbeddedDocumentField(NutritionFact)
    sources = me.EmbeddedDocumentListField(DataSource)

    created_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow)
    updated_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow,
                                    auto_now=True)

    meta = {'collection': 'nutritions'}

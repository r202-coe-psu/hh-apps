import mongoengine as me
import datetime

from .common import User
from .items import Item
from .stocks import Stock


class Inventory(me.Document):
    item = me.ReferenceField(Item)
    adder = me.EmbeddedDocumentField(User)
    stock = me.ReferenceField(Stock)

    quantity = me.IntField(required=True, default=0)
    serving_size_quantity = me.FloatField(required=True, default=0)
    serving_size_unit = me.StringField(required=True, default='can')
    total_serving_size = me.FloatField(required=True, default=0)
    available_serving_size = me.FloatField(required=True, default=0)

    status = me.StringField(required=True, default='deactivate')
    meta = me.DictField()

    expired_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow)
    created_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow)
    updated_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow,
                                    auto_now=True)

    consumptions = me.ListField(me.ReferenceField('Consumption', dbref=True))

    meta = {'collection': 'inventories'}


class Consumption(me.Document):
    consuming_size = me.FloatField(required=True, default=0)
    consuming_unit = me.StringField(required=True)
    consuming_date = me.DateTimeField(required=True,
                                      default=datetime.datetime.utcnow)
    inventory = me.ReferenceField(Inventory, required=True, dbref=True)
    stock = me.ReferenceField(Stock, required=True, dbref=True)
    item = me.ReferenceField(Item, required=True, dbref=True)

    consumer = me.EmbeddedDocumentField(User)
    status = me.StringField(required=True, default='deactivate')

    meta = {'collection': 'consumptions'}

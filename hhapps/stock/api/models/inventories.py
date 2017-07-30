import mongoengine as me
import datetime

from .common import User
from .items import Item
from .stocks import Stock


class ConsumedLog(me.EmbeddedDocument):
    id = me.ObjectIdField(required=True)
    consumed_size = me.FloatField(required=True, default=0)
    consumed_unit = me.StringField(required=True)
    consumed_date = me.DateTimeField(required=True,
                                     default=datetime.datetime.utcnow)

    consumer = me.EmbeddedDocumentField(User)


class Inventory(me.Document):
    item = me.ReferenceField(Item)
    adder = me.EmbeddedDocumentField(User)
    stock = me.ReferenceField(Stock)

    quantity = me.IntField(required=True, default=0)
    serving_size_quantity = me.FloatField(required=True, default=0)
    serving_size_unit = me.StringField(required=True, default='can')
    consuming_size = me.FloatField(required=True, default=0)

    status = me.StringField(required=True, default='deactivate')
    meta = me.DictField()

    expired_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow)
    created_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow)
    updated_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow,
                                    auto_now=True)

    consumed_log = me.EmbeddedDocumentListField(ConsumedLog)

    meta = {'collection': 'inventories'}

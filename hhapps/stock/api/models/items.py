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


class Item(me.Document):
    name = me.StringField(required=True)
    description = me.StringField()
    tags = me.ListField(me.StringField())

    brand = me.ReferenceField(Brand)
    manufactory = me.ReferenceField(Manufactory)

    meta = me.DictField()

    upc = me.StringField(uniqued=True)

    user = me.EmbeddedDocumentField(User)

    status = me.StringField(required=True, default='deactivate')

    created_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow)
    updated_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow,
                                    auto_now=True)

    meta = {'collection': 'items'}

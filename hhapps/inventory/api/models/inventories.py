import mongoengine as me
import datetime


class User(me.EmbeddedDocument):
    id = me.ObjectIdField(required=True)


class Building(me.EmbeddedDocument):
    id = me.ObjectIdField(required=True)


class Inventory(me.Document):
    name = me.StringField(required=True)
    description = me.StringField()
    tags = me.ListField(me.StringField())

    owner = me.EmbeddedDocumentField(User)
    building = me.EmbeddedDocumentField(Building)

    status = me.StringField(required=True, default='deactivate')

    created_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow)
    updated_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow,
                                    auto_now=True)

    meta = {'collection': 'inventories'}

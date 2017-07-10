import mongoengine as me
import datetime


class Inventory(me.Document):

    name = me.StringField(required=True)
    description = me.StringField()
    tags = me.ListField(me.StringField())

    owner_id = me.ObjectIdField(required=True)
    
    status = me.StringField(required=True, default='deactivate')

    created_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow)
    updated_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow,
                                    auto_now=True)

    meta = {'collection': 'inventories'}

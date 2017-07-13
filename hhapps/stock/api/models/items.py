import mongoengine as me
import datetime

from 


class Item(me.Document):
    name = me.StringField(required=True)
    description = me.StringField()
    tags = me.ListField(me.StringField())

    upc = me.StringField(uniqued=True)

    user = me.EmbeddedDocumentField(User)

    status = me.StringField(required=True, default='deactivate')

    created_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow)
    updated_date = me.DateTimeField(required=True,
                                    default=datetime.datetime.utcnow,
                                    auto_now=True)

    meta = {'collection': 'items'}

import mongoengine as me


class User(me.EmbeddedDocument):
    id = me.ObjectIdField(required=True)


class Building(me.EmbeddedDocument):
    id = me.ObjectIdField(required=True)

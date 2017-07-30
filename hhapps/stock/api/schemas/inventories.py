from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema

from . import common
from . import items


class InventorySchema(Schema):

    id = fields.String(dump_only=True)
    item = fields.Relationship(
            related_url='/items/{item_id}',
            related_url_kwargs={'item_id': '<id>'},
            many=False,
            schema=items.ItemSchema,
            include_resource_linkage=True,
            type_='items',
            allow_none=True
            )
    item_upc = fields.String(allow_none=True)
    quantity = fields.Integer(required=True)
    expired_date = fields.DateTime()

    status = fields.String(requred=True, dump_only=True, default='deactive')

    adder = fields.Relationship(
            related_url='/users/{user_id}',
            related_url_kwargs={'user_id': '<id>'},
            many=False,
            schema=common.UserSchema,
            include_resource_linkage=True,
            type_='users',
            dump_only=True
            )

    created_date = fields.DateTime(dump_only=True)
    updated_date = fields.DateTime(dump_only=True)

    class Meta:
        type_ = 'inventories'
        strict = True
        inflect = common.dasherize

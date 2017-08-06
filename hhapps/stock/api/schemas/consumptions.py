from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema

from . import common
from . import items
from . import stocks
from . import inventories


class ConsumptionSchema(Schema):
    id = fields.String(dump_only=True)
    consuming_size = fields.Float()
    consuming_unit = fields.String()
    consuming_date = fields.DateTime(dump_only=True)

    inventory = fields.Relationship(
            related_url='/inventories/{inventory_id}',
            related_url_kwargs={'inventory_id': '<id>'},
            many=False,
            schema=inventories.InventorySchema,
            include_resource_linkage=True,
            type_='inventories',
            dump_only=True
            )
    stock = fields.Relationship(
            related_url='/stocks/{stock_id}',
            related_url_kwargs={'stock_id': '<id>'},
            many=False,
            schema=stocks.StockSchema,
            include_resource_linkage=True,
            type_='stocks',
            dump_only=True
            )
    item = fields.Relationship(
            related_url='/items/{item_id}',
            related_url_kwargs={'item_id': '<id>'},
            many=False,
            schema=items.ItemSchema,
            include_resource_linkage=True,
            type_='items',
            dump_only=True
            )
    consumer = fields.Relationship(
            related_url='/users/{user_id}',
            related_url_kwargs={'user_id': '<id>'},
            many=False,
            schema=common.UserSchema,
            include_resource_linkage=True,
            type_='users',
            dump_only=True
            )
    status = fields.String()

    class Meta:
        type_ = 'consumptions'
        strict = True
        inflect = common.dasherize

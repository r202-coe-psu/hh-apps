from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema

from . import common
from . import items
from . import stocks


class InventoryConsumingItemSchema(Schema):
    id = fields.String(dump_only=True, allow_none=True)
    item = fields.Relationship(
            related_url='/items/{item_id}',
            related_url_kwargs={'item_id': '<id>'},
            many=False,
            schema=items.ItemSchema,
            include_resource_linkage=True,
            type_='items',
            )
    consuming_size = fields.Integer()

    class Meta:
        type_ = 'inventory-consuming-items'
        strict = True
        inflect = common.dasherize


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
    consuming_size = fields.Float(dump_only=True)
    serving_size_quantity = fields.Float(dump_only=True)
    serving_size_unit = fields.String(dump_only=True)
    total_serving_size = fields.Float(dump_only=True)
    available_serving_size = fields.Float(dump_only=True)

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


class ConsumingLog(Schema):
    id = fields.String(dump_only=True)
    consuming_size = fields.Float()
    consuming_unit = fields.String()
    consuming_date = fields.DateTime(dump_only=True)

    inventory = fields.Relationship(
            related_url='/inventories/{inventory_id}',
            related_url_kwargs={'inventory_id': '<id>'},
            many=False,
            # schema=Inventory,
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
        type_ = 'consuming-logs'
        strict = True
        inflect = common.dasherize


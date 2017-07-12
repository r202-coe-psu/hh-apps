import marshmallow as ma
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema

from . import common

class InventorySchema(Schema):

    id = fields.String(dump_only=True)
    name = fields.String(required=True,
                         validator=ma.validate.Length(min=3, max=20))
    description = fields.String()
    tags = fields.List(fields.String())

    status = fields.String(requred=True, default='deactive')

    owner = fields.Relationship(
            related_url='/users/{user_id}',
            related_url_kwargs={'user_id': '<id>'},
            many=False,
            schema=common.UserSchema,
            include_resource_linkage=True,
            type_='users',
            dump_only=True
            )
    building = fields.Relationship(
            related_url='/buildings/{building_id}',
            related_url_kwargs={'building_id': '<id>'},
            many=False,
            schema=common.BuildingSchema,
            include_resource_linkage=True,
            type_='buildings',
            )

    created_date = fields.DateTime(dump_only=True)
    updated_date = fields.DateTime(dump_only=True)

    class Meta:
        type_ = 'inventories'
        strict = True
        inflect = common.dasherize

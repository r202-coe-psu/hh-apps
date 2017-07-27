import marshmallow as ma
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema

from . import common


class ItemSchema(Schema):

    id = fields.String(dump_only=True)
    name = fields.String(required=True,
                         validator=ma.validate.Length(min=3, max=20))
    description = fields.String()
    tags = fields.List(fields.String())
    upc = fields.String()
    color = fields.String()
    size = fields.String()
    weight = fields.String()
    dimension = fields.String()
    category = fields.String()
    image = fields.URL()

    manufactory = fields.String()
    meta = fields.Dict()

    status = fields.String(requred=True, default='deactive')

    created_date = fields.DateTime(dump_only=True)
    updated_date = fields.DateTime(dump_only=True)

    class Meta:
        type_ = 'items'
        strict = True
        inflect = common.dasherize

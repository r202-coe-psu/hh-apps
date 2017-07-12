import marshmallow as ma
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema


def dasherize(text):
    return text.replace('_', '-')


class UserSchema(Schema):

    id = fields.String()

    class Meta:
        type_ = 'users'
        strict = True
        inflect = dasherize


class BuildingSchema(Schema):

    id = fields.String()

    class Meta:
        type_ = 'buildings'
        strict = True
        inflect = dasherize

import marshmallow_jsonschema as mjs
import marshmallow_jsonapi as mja
from marshmallow import fields
import datetime


def dasherize(text):
        return text.replace('_', '-')


class JSONAPISchema(mjs.JSONSchema):

    def get_properties(self, obj):
        mapping = {v: k for k, v in obj.TYPE_MAPPING.items()}
        mapping[fields.Email] = mjs.base.text_type
        mapping[fields.Dict] = dict
        mapping[fields.List] = list
        mapping[fields.Url] = mjs.base.text_type
        mapping[fields.LocalDateTime] = datetime.datetime
        properties = {}

        for field_name, field in sorted(obj.fields.items()):
            # print('ff', field_name, field.__class__)
            if hasattr(field, '_jsonschema_type_mapping'):
                schema = field._jsonschema_type_mapping()
            elif field.__class__ in mapping:
                pytype = mapping[field.__class__]
                schema = self.__class__._from_python_type(field, pytype)
            elif isinstance(field, fields.Nested):
                schema = self.__class__._from_nested_schema(field)
            elif isinstance(field, mja.fields.Relationship):
                # print(field_name, field)
                try:
                    schema = self.__class__._from_relationship_type(field)
                except Exception as e:
                    print('rr', e)
            else:
                raise ValueError('unsupported field type %s' % field)

            # Apply any and all validators that field may have
            for validator in field.validators:
                if validator.__class__ in mjs.base.FIELD_VALIDATORS:
                    schema = mjs.base.FIELD_VALIDATORS[validator.__class__](
                        schema, field, validator, obj
                    )

            properties[field.name] = schema

        # print('properties', properties)
        new_properties = {}
        for k, v in properties.items():
            if 'type' in v and v['type'] == 'array':
                field = obj.fields[k].container.__class__
                if field == fields.String:
                    v['items'] = dict(type='string')
            if 'title' in v:
                v['title'] = dasherize(v['title'])

            new_properties[dasherize(k)] = v
        return new_properties

    def get_required(self, obj):
        required = [t.replace('_', '-') for t in super().get_required(obj)]

        return required

    @classmethod
    def _from_relationship_type(cls, field):
        schema = cls().dump(field).data

        if field.metadata.get('metadata', {}).get('description'):
            schema['description'] = (
                field.metadata['metadata'].get('description')
            )

        if field.metadata.get('metadata', {}).get('title'):
            schema['title'] = field.metadata['metadata'].get('title')

        sub_schema = None
        if field._Relationship__schema:
            sub_schema = cls().dump(field._Relationship__schema()).data

        if sub_schema:
            meta = {'jsonapitype': field._Relationship__schema.Meta.type_}
            sub_schema['meta'] = meta
            print('sbs', sub_schema)

        if field.many:
            schema = {
                'type': ["array"] if field.required else ['array', 'null'],
                'items': sub_schema,
            }
        else:
            if sub_schema:
                schema.update(sub_schema)

        return schema

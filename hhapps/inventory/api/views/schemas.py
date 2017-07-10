from flask import Blueprint

from hhapps.common.renderers import render_json
from hhapps.common.json_schemas import JSONAPISchema
from hhapps.inventory.api import schemas


module = Blueprint('schemas', __name__, url_prefix='/schemas')


@module.route('')
def all():
    json_schema = JSONAPISchema()

    schema_list = schemas.__all__

    all_schemas = {}
    for schema in schema_list:
        all_schemas[schema.Meta.type_] = json_schema.dump(schema()).data

    return render_json(all_schemas)

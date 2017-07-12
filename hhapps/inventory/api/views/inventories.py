from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, current_user

from hhapps.inventory.api import models
from hhapps.inventory.api import schemas
from hhapps.common.renderers import render_json

module = Blueprint('inventoriess', __name__, url_prefix='/inventories')


def get_inventory_error_not_found():
    response_dict = request.get_json()
    errors = [
        {
            'status': '404',
            'title':  'Inventory not found',
            'detail': 'Inventory not found'
        }
    ]
    response_dict.update(errors=errors)
    response = render_json(response_dict)
    response.status_code = 404

    return response


@module.route('', methods=['POST'])
@jwt_required
def create():
    schema = schemas.InventorySchema()
    print('got', request.get_json())
    try:
        inventory_data = schema.load(request.get_json())
    except Exception as e:
        print(e)
        response_dict = request.get_json()
        response_dict.update(e.messages)
        response = render_json(response_dict)
        response.status_code = 400
        abort(response)
    data = inventory_data.data
    data['building'] = models.Building(id=data['building'])
    data['owner'] = models.User(id=current_user.id)
    
    inventory = models.Inventory(status='active',
                                 **data)
    inventory.save()

    return render_json(schema.dump(inventory).data)


@module.route('', methods=['GET'])
@jwt_required
def list():
    schema = schemas.InventorySchema(many=True)
    owner_id = current_user.id
    inventories = models.Inventory.objects(owner_id=owner_id)
    return render_json(schema.dump(inventories).data)


@module.route('/<inventory_id>', methods=['GET'])
@jwt_required
def get(inventory_id):
    schema = schemas.InventorySchema()
    owner = current_user
    inventory = models.Inventory.objects(id=inventory_id,
                                         owner__id=owner.id).first()
    if not inventory:
        return abort(get_inventory_error_not_found())

    return render_json(schema.dump(inventory).data)


@module.route('/<inventory_id>', methods=['DELETE'])
@jwt_required
def delete(inventory_id):
    owner = current_user._get_current_object()
    inventory = models.Inventory.objects(id=inventory_id,
                                         owner=owner).first()
    if not inventory:
        return abort(get_inventory_error_not_found())

    inventory.delete()

    return render_json()

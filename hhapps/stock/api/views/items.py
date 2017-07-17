from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, current_user

from hhapps.stock.api import models
from hhapps.stock.api import schemas
from hhapps.common.renderers import render_json

module = Blueprint('items', __name__, url_prefix='/items')


def get_item_error_not_found():
    response_dict = request.get_json()
    errors = [
        {
            'status': '404',
            'title':  'Item not found',
            'detail': 'Item not found'
        }
    ]
    response_dict.update(errors=errors)
    response = render_json(response_dict)
    response.status_code = 404

    return response


@module.route('', methods=['POST'])
@jwt_required
def create():
    schema = schemas.ItemSchema()
    print('got', request.get_json())
    try:
        stock_data = schema.load(request.get_json())
    except Exception as e:
        print(e)
        response_dict = request.get_json()
        response_dict.update(e.messages)
        response = render_json(response_dict)
        response.status_code = 400
        abort(response)
    data = stock_data.data
    data['building'] = models.Building(id=data['building'])
    data['owner'] = models.User(id=current_user.id)

    stock = models.Item(status='active',
                        **data)
    stock.save()

    return render_json(schema.dump(stock).data)


@module.route('', methods=['GET'])
@jwt_required
def list():
    schema = schemas.ItemSchema(many=True)
    items = models.Item.objects(status='active')

    return render_json(schema.dump(items).data)


@module.route('/<stock_id>', methods=['GET'])
@jwt_required
def get(stock_id):
    schema = schemas.ItemSchema()
    owner = current_user
    stock = models.Item.objects(id=stock_id,
                                owner__id=owner.id).first()
    if not stock:
        return abort(get_item_error_not_found())

    return render_json(schema.dump(stock).data)


@module.route('/<stock_id>', methods=['DELETE'])
@jwt_required
def delete(stock_id):
    owner = current_user._get_current_object()
    stock = models.Item.objects(id=stock_id,
                                owner=owner).first()
    if not stock:
        return abort(get_item_error_not_found())

    stock.delete()

    return render_json()

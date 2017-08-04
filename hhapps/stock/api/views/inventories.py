from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, current_user

from hhapps.stock.api import models
from hhapps.stock.api import schemas
from hhapps.common.renderers import render_json
from . import items

module = Blueprint('inventories',
                   __name__,
                   url_prefix='/stocks/<stock_id>/inventories')


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
def create(stock_id):
    adder = current_user._get_current_object()
    schema = schemas.InventorySchema()

    stock = models.Stock.objects.with_id(stock_id)
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

    print('data:', data)
    data['adder'] = adder
    data['stock'] = stock

    item = None
    if data['item'] and len(data['item']) > 0:
        try:
            item = models.Item.objects.with_id(data['item'])
        except:
            pass
    elif len(data['item_upc']) > 0:
        item = models.Item.objects(upc=data['item_upc']).first()
        if not item:
            item = items.add_item(data['item_upc'])

    if not item:
        return abort(items.get_item_not_found_error())

    data['item'] = item
    data.pop('item_upc')

    inventory = models.Inventory(status='active',
                                 **data)
    nutrition = models.Nutrition.objects(item=item).first()

    if nutrition:
        inventory.serving_size_unit = nutrition.facts.serving_size_unit
        inventory.serving_size_quantity = nutrition.facts.serving_size_quantity
        inventory.total_serving_size = data['quantity'] * \
            nutrition.facts.servings_per_container
        inventory.available_serving_size = inventory.total_serving_size

    inventory.save()

    return render_json(schema.dump(inventory).data)


@module.route('', methods=['GET'])
@jwt_required
def list(stock_id):
    schema = schemas.InventorySchema(many=True)
    stock = models.Stock.objects.with_id(stock_id)

    inventories = models.Inventory.objects(stock=stock)

    return render_json(schema.dump(inventories).data)


@module.route('/<inventory_id>', methods=['GET'])
@jwt_required
def get(stock_id, inventory_id):
    schema = schemas.InventorySchema()
    owner = current_user
    stock = models.Inventory.objects(id=stock_id,
                                     owner__id=owner.id).first()
    if not stock:
        return abort(get_inventory_error_not_found())

    return render_json(schema.dump(stock).data)


@module.route('/<inventory_id>', methods=['DELETE'])
@jwt_required
def delete(stock_id, inventory_id):
    owner = current_user._get_current_object()
    stock = models.Inventory.objects(id=stock_id,
                                     owner=owner).first()
    if not stock:
        return abort(get_inventory_error_not_found())

    stock.delete()

    return render_json()


@module.route('/list-items', methods=['GET'])
@jwt_required
def list_items(stock_id):
    schema = schemas.ItemSchema(many=True)
    stock = models.Stock.objects.with_id(stock_id)

    inventories = models.Inventory.objects(stock=stock, status='active')
    items = set([inventory.item for inventory in inventories])

    return render_json(schema.dump(items).data)


@module.route('/consume', methods=['POST'])
def consume(stock_id):
    stock = models.Stock.objects.with_id(stock_id)
    schema = schemas.ConsumingItemSchema()

    try:
        consuming_data = schema.load(request.get_json())
    except Exception as e:
        print(e)
        response_dict = request.get_json()
        response_dict.update(e.messages)
        response = render_json(response_dict)
        response.status_code = 400
        abort(response)

    item = models.Item.objects.with_id(id=consuming_data.item)
    inventories = models.Inventory.objects(stock=stock,
                                           item=item,
                                           status='active')

    return render_json(schema.dump(items).data)


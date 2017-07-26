from flask import Blueprint, request, abort, g
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
    if not response_dict:
        response_dict = {}
    response_dict.update(errors=errors)
    response = render_json(response_dict)
    response.status_code = 404

    return response


NUTRITIONIX_ALLERGEN_MAPPER = {
    'allergen_contains_eggs': 'eggs',
    'allergen_contains_fish': 'fish',
    'allergen_contains_gluten': 'gluten',
    'allergen_contains_milk': 'milk',
    'allergen_contains_peanuts': 'peanuts',
    'allergen_contains_shellfish': 'shellfish',
    'allergen_contains_soybeans': 'soybeans',
    'allergen_contains_tree_nuts': 'nuts',
    'allergen_contains_wheat': 'wheat'
}

NUTRITIONIX_NUTRITION_FACT_MAPPER = {
    'nf_calcium_dv': 'calcium_dv',
    'nf_calories': 'calories',
    'nf_calories_from_fat': 'calories_from_fat',
    'nf_cholesterol': 'cholesterol',
    'nf_dietary_fiber': 'dietary_fiber',
    'nf_ingredient_statement': 'ingredient_statement',
    'nf_iron_dv': 'iron_dv',
    'nf_monounsaturated_fat': 'monounsaturated_fat',
    'nf_polyunsaturated_fat': 'polyunsaturated_fat',
    'nf_protein': 'protein',
    'nf_refuse_pct': 'refuse_pct',
    'nf_saturated_fat': 'saturated_fat',
    'nf_serving_size_qty': 'serving_size_qty',
    'nf_serving_size_unit': 'serving_size_unit',
    'nf_serving_weight_grams': 'serving_weight_grams',
    'nf_servings_per_container': 'servings_per_container',
    'nf_sodium': 'sodium',
    'nf_sugars': 'sugars',
    'nf_total_carbohydrate': 'total_carbohydrate',
    'nf_total_fat': 'total_fat',
    'nf_trans_fatty_acid': 'trans_fatty_acid',
    'nf_vitamin_a_dv': 'vitamin_a_dv',
    'nf_vitamin_c_dv': 'vitamin_c_dv',
    'nf_water_grams': 'water_grams',
}


@module.route('', methods=['POST'])
@jwt_required
def create():
    schema = schemas.ItemSchema()
    try:
        item_data = schema.load(request.get_json())
    except Exception as e:
        print(e)
        response_dict = request.get_json()
        response_dict.update(e.messages)
        response = render_json(response_dict)
        response.status_code = 400
        abort(response)
    data = item_data.data
    data['building'] = models.Building(id=data['building'])
    data['owner'] = models.User(id=current_user.id)

    item = models.Item(status='active',
                       **data)
    item.save()

    return render_json(schema.dump(item).data)


@module.route('', methods=['GET'])
@jwt_required
def list():
    schema = schemas.ItemSchema(many=True)

    items = models.Item.objects(status='active')

    return render_json(schema.dump(items).data)


@module.route('/<item_id>', methods=['GET'])
@jwt_required
def get(item_id):
    schema = schemas.ItemSchema()
    item = models.Item.objects(id=item_id).first()
    if not item:
        return abort(get_item_error_not_found())

    return render_json(schema.dump(item).data)


@module.route('/<item_id>', methods=['DELETE'])
@jwt_required
def delete(item_id):
    owner = current_user._get_current_object()
    item = models.Item.objects(id=item_id,
                               owner=owner).first()
    if not item:
        return abort(get_item_error_not_found())

    item.delete()

    return render_json()


@module.route('/upc/<upc>', methods=['GET'])
def get_upc(upc):

    schema = schemas.ItemSchema()
    item = models.Item.objects(upc=upc).first()
    if not item:
        item = add_item(upc)

    if not item:
        return abort(get_item_error_not_found())

    return render_json(schema.dump(item).data)


def add_item_from_upcitemdb(upc):
    response = g.upcitemdb.lookup(upc=upc)

    # import pprint
    # print('upcitemdb')
    # pprint.pprint(response)

    item = None
    if response['code'] != 'INVALID_UPC':
        item_upcitemdb = response['items'][0]
        brand = models.Brand.objects(
                name=item_upcitemdb['brand']).first()
        if not brand:
            brand = models.Brand(name=item_upcitemdb['brand'])
            brand.save()
            brand.reload()

        item_upcitemdb.pop('offers')
        data_source = models.DataSource(data=item_upcitemdb,
                                        provider='upcitemdb')

        item = models.Item(
                name=item_upcitemdb['title'],
                description=item_upcitemdb['description'],
                upc=upc,
                color=item_upcitemdb['color'],
                size=item_upcitemdb['size'],
                dimension=item_upcitemdb['dimension'],
                weight=item_upcitemdb['weight'],
                brand=brand,
                sources=[data_source],
                category='food',
                status='active'
                )
        item.save()

    return item


def add_item_from_nutritionix(upc, item=None):

    item_nutritionix = g.nutritionix.item(upc=upc)

    # import pprint
    # print('nutritionix')
    # pprint.pprint(item_nutritionix)

    if 'status_code' in item_nutritionix \
            and item_nutritionix['status_code'] == 404:
        abort(get_item_error_not_found())

        data_source = models.DataSource(data=item_nutritionix,
                                        provider='nutritionix')
        if not item:
            brand = models.Brand.objects(
                    name=item_nutritionix['brand_name']).first()
            if not brand:
                brand = models.Brand(name=item_nutritionix['brand_name'])
                brand.save()
                brand.reload()

            item = models.Item(
                    name=item_nutritionix['item_name'],
                    description=item_nutritionix['item_description'],
                    upc=upc,
                    brand=brand,
                    category='food',
                    sources=[data_source],
                    status='active')
            item.save()
            item.reload()

        allergen = models.Allergen()
        for k, mk in NUTRITIONIX_ALLERGEN_MAPPER.items():
            setattr(allergen, mk, item_nutritionix[k])

        nutrition_fact = models.NutritionFact()
        for k, mk in NUTRITIONIX_NUTRITION_FACT_MAPPER.items():
            setattr(nutrition_fact, mk, item_nutritionix[k])

        nutrition = models.Nutrition(item=item,
                                     allergen=allergen,
                                     facts=nutrition_fact,
                                     sources=[data_source])

        nutrition.save()

    return item


def add_item(upc):
    item = add_item_from_upcitemdb(upc)
    item = add_item_from_nutritionix(upc, item)

    return item

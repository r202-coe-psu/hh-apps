from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, current_user

from hhapps.stock.api import models
from hhapps.stock.api import schemas
from hhapps.common.renderers import render_json

module = Blueprint('consumptions',
                   __name__,
                   url_prefix='/stocks/<stock_id>/consumptions')


@module.route('', methods=['GET'])
@jwt_required
def list(stock_id):
    stock = models.Stock.objects.with_id(stock_id)
    consumptions = models.Consumption.objects(
            stock=stock).order_by('+consumed_data')

    schema = schemas.ConsumptionSchema(many=True)
    return render_json(schema.dump(consumptions).data)

from flask import Blueprint
__author__ = 'YohnCF'


item_blueprint = Blueprint('item', __name__)


@item_blueprint.route('/<string:name>')
def item_page():
    pass


from flask import Blueprint, render_template, request, json, redirect, url_for

from src.models.stores.store import Store
from src.decorators import requires_admin

__author__ = 'YohnCF'

store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/')
def index():
    stores = Store.all()
    return render_template('stores/store_list.jinja2', stores=stores)


@store_blueprint.route('/store/<string:store_id>')
def store_page(store_id):
    return render_template('stores/store.jinja2', store=Store.get_by_id(store_id))


@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@requires_admin
def edit_store(store_id):
    store = Store.get_by_id(store_id)
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url']
        price_tag = request.form['price_tag']
        price_query = json.loads(request.form['price_query'])
        name_tag = request.form['name_tag']
        name_query = json.loads(request.form['name_query'])

        store.name = name
        store.url_prefix =url_prefix
        store.p_tag_name = price_tag
        store.p_query = price_query
        store.n_tag_name = name_tag
        store.n_query = name_query

        store.save_to_db()
        return redirect(url_for('.store_page', store_id=store_id))

    return render_template('stores/edit_store.jinja2', store=store)


@store_blueprint.route('/delete/<string:store_id>', methods=['GET', 'POST'])
@requires_admin
def delete_store(store_id):
        Store.get_by_id(store_id).delete()
        return redirect(url_for('.index'))


@store_blueprint.route('/new',methods=['GET', 'POST'])
@requires_admin
def create_store():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url']
        price_tag = request.form['price_tag']
        price_query = json.loads(request.form['price_query'])
        name_tag = request.form['name_tag']
        name_query = json.loads(request.form['name_query'])

        Store(name, url_prefix, price_tag, price_query, name_tag, name_query).save_to_db()

        return redirect(url_for('.index'))

    return render_template('stores/create_store.jinja2')
from flask import Blueprint, render_template, request, session, redirect, url_for
from src.models.alerts.alert import Alert
from src.models.items.item import Item
from src.decorators import requires_login

__author__ = 'YohnCF'


alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/')
def index():
    return render_template('alerts/alerts_home.jinja2')


@alert_blueprint.route('/new', methods=['GET', 'POST'])
@requires_login
def create_alert():
    if request.method == 'POST':
        name = request.form['item_name']
        url = request.form['item_url']
        price = float(request.form['price'])

        new_item = Item(url, name)
        new_item.save_to_db()

        alert = Alert(session['email'], price, new_item._id)
        alert.load_item_price()  # This already saves to DB.
        return redirect('users/alerts')

    return render_template('alerts/create_alert.jinja2')


@alert_blueprint.route('/deactivate/<string:alert_id>')
@requires_login
def deactivate_alert(alert_id):
    Alert.get_by_id(alert_id).deactivate()
    return redirect(url_for('.get_alert_page',alert_id=alert_id))


@alert_blueprint.route('/activate/<string:alert_id>')
@requires_login
def activate_alert(alert_id):
    Alert.get_by_id(alert_id).activate()
    return redirect(url_for('.get_alert_page',alert_id=alert_id))


@alert_blueprint.route('/delete/<string:alert_id>')
@requires_login
def delete_alert(alert_id):
    Alert.get_by_id(alert_id).delete()
    return redirect(url_for('user.user_alerts'))


@alert_blueprint.route('/<string:alert_id>')
@requires_login
def get_alert_page(alert_id):
    return render_template('alerts/alert.jinja2', alert=Alert.get_by_id(alert_id))


@alert_blueprint.route('/check_price/<string:alert_id>')
@requires_login
def check_price(alert_id):
    Alert.get_by_id(alert_id).load_item_price()
    return redirect(url_for('.get_alert_page', alert_id=alert_id))


@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
@requires_login
def edit_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    if request.method == 'POST':
        alert.price_limit = float(request.form['price'])
        alert.save_to_db()
        return redirect(url_for('.get_alert_page', alert_id=alert_id))

    return render_template('alerts/edit_alert.jinja2', alert=alert)
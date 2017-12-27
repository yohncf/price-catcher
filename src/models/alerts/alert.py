import datetime
import uuid
import requests
import src.models.alerts.constants as AlertConstants
from src.common.database import Database
from src.models.items.item import Item

__author__ = 'YohnCF'


class Alert(object):
    def __init__(self, user_email, price_limit, item_id, active=True, last_checked=None, _id=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.get_by_id(item_id)
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id
        self.active = active

    def __repr__(self):
        return "<Alert for {} on item {}with price {}>".format(self.user_email, self.item.name, self.price_limit)

    def send(self):
        return requests.post(
            AlertConstants.URL,
            auth=("api", AlertConstants.API_KEY),
            data={
                "from": AlertConstants.FROM,
                "to": self.user_email,
                "subject": "Price limit reached for{}".format(self.item.name),
                "text": "we found a deal! (link here)".format(self.item.url)
            })

    @classmethod
    def find_last_update(cls, minutes_since_update=AlertConstants.TIMEOUT):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_since_update)
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION,
                                                      {"last_checked":
                                                           {"$lte": last_updated_limit},
                                                       "active": True
                                                       })]

    def save_to_db(self):
        Database.update(AlertConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "user_email": self.user_email,
            "price_limit": self.price_limit,
            "item_id": self.item._id,
            "last_checked": self.last_checked,
            "active": self.active
        }

    def load_item_price(self):
        self.item.load_price()
        self.last_checked = datetime.datetime.utcnow()
        self.item.save_to_db()
        self.save_to_db()
        return self.item.price

    def send_email_price_reached(self):
        if self.item.price < self.price_limit:
            self.send()

    @classmethod
    def find_by_user_email(cls, user_email):
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, {'user_email': user_email})]

    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one(AlertConstants.COLLECTION,{"_id": _id}))

    def deactivate(self):
        self.active = False
        self.save_to_db()

    def activate(self):
        self.active = True
        self.save_to_db()

    def delete(self):
        Database.remove(AlertConstants.COLLECTION, { "_id": self._id })
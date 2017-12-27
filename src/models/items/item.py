import re
import uuid

import requests
from bs4 import BeautifulSoup
import src.models.items.constants as ItemConstants
from src.common.database import Database
from src.models.stores.store import Store

__author__ = 'YohnCF'


class Item(object):
    def __init__(self, url, name=None, price=None, _id=None):
        self.url = url
        store = Store.get_by_full_url(url)
        n_tag_name = store.n_tag_name
        n_query = store.n_query
        self.name = self.load_name(n_tag_name, n_query) if name is None else name
        self.p_tag_name = store.p_tag_name
        self.p_query = store.p_query
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "< Item {} with URL {}>".format(self.name, self.url)

    def load_name(self, n_tag_name, n_query):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, 'html.parser')
        element = soup.find(n_tag_name, n_query)
        string_name = element.text().strip()

        return string_name

    def load_price(self):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, 'html.parser')
        element = soup.find(self.p_tag_name, self.p_query)
        string_price = element.text.strip().replace(',','')

        pattern = re.compile("(\d.+\d)")
        match = pattern.search(string_price)
        self.price = float(match.group())
        return self.price

    def save_to_db(self):
        Database.update(ItemConstants.COLLECTION, {'_id': self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url": self.url,
            "price": self.price
        }

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": item_id}))

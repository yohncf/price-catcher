import uuid
from src.common.database import Database
import src.models.stores.constants as StoreConstants
import src.models.stores.errors as StoreErrors

__author__ = 'YohnCF'


class Store(object):
    def __init__(self, name, url_prefix, p_tag_name, p_query, n_tag_name, n_query, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.p_tag_name = p_tag_name
        self.p_query = p_query
        self.n_tag_name = n_tag_name
        self.n_query = n_query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def save_to_db(self):
        Database.update(StoreConstants.COLLECTION, {'_id':self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "n_tag_name": self.n_tag_name,
            "n_query": self.n_query,
            "p_tag_name": self.p_tag_name,
            "p_query": self.p_query
        }

    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"_id": _id}))

    @classmethod
    def get_by_name(cls, store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"name": store_name}))

    @classmethod
    def get_by_url(cls, url_prefix):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"url_prefix": {"$regex": '^{}'.format(url_prefix)}}))

    @classmethod
    def get_by_full_url(cls, full_url):
        for i in range(0, len(full_url)+1):
            try:
                store = cls.get_by_url(full_url[:1])
                return store
            except:
                raise StoreErrors.StoreNotFoundException("The URL didn't give any results")

    @classmethod
    def all(cls):
        return  [cls(**elem) for elem in Database.find(StoreConstants.COLLECTION, {})]

    def delete(self):
        Database.remove(StoreConstants.COLLECTION, {"_id":self._id})
import uuid

from src.models.alerts.alert import Alert
from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as err
import src.models.users.constants as UserConstants
__author__ = 'YohnCF'


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email, password):  # Password in sha512 -> pbkdf2_sha512
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if user_data is None:
            # Tell User email doesn't exist
            raise err.UserNotExistError("Your user does not exists.")
        if not Utils.check_hash_password(password, user_data['password']):
            # Tell the user that their password is wrong
            raise err.IncorrectPassword("Your password was wrong.")
        return True

    @staticmethod
    def register_user(email,password):
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if user_data is not None:
            # Tell User they are already registered
            raise err.UserAlreadyRegister("The email you used already exists")
        if not Utils.email_is_valid(email):
            # Tell user that their email is not constructed properly
            raise err.InvalidEmailError("The email does not have the right format")
        User(email, Utils.hash_pasword(password)).save_to_db()
        return True

    def save_to_db(self):
        Database.insert('users', self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls,email):
        return cls(**Database.find_one(UserConstants.COLLECTION,{'email':email}))

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)
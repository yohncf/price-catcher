from passlib.hash import pbkdf2_sha512
import re
__author__ = 'YohnCF'


class Utils(object):

    @staticmethod
    def hash_pasword(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: The sha512 password from the login/register form
        :return: A pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hash_password(password, hashed_password):
        """
        Check that the password the user sent matches that of the database.
        the database password is encrypted.
        :param password: sha512-hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if password match, False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('([\w.-]+)+@([\w.-]+\.)+[\w]')
        return True if email_address_matcher.match(email) else False

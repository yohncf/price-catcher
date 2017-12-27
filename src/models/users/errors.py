__author__ = 'YohnCF'


class UserError(Exception):
    def __init__(self, message):
        self.message = message


class UserNotExistError(UserError):
    pass


class IncorrectPassword(UserError):
    pass


class UserAlreadyRegister(UserError):
    pass


class InvalidEmailError(UserError):
    pass

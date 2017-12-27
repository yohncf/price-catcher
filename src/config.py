import os

__author__ = 'YohnCF'


DEBUG = True
ADMINS = frozenset([
    os.environ.get('MAIL')
])

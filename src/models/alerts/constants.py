import os

__author__ = 'YohnCF'

URL = os.environ.get('MAILGUN_URL')
API_KEY = os.environ.get('MAILGUN_API_KEY')
FROM = os.environ.get('MAILGUN_FROM')
TIMEOUT = 10
COLLECTION = "alerts"

# coding: utf-8

"""
Model utility methods
"""

import locale
from datetime import datetime
from datetime import timedelta

from django.conf import settings


def get_delta():
    """
    Returns the date before now in settings.OFFER_EXPIRATION_LIMIT days
    """
    now = datetime.now()
    return now - timedelta(days=settings.OFFER_EXPIRATION_LIMIT)


def pretty_price(value, spacing=' '):
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    return '$' + spacing + locale.format("%d", value, True).replace(',', '.')
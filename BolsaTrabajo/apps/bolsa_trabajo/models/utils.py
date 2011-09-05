# coding: utf-8

"""
Model utility methods
"""

import locale
import datetime

from django.conf import settings


def get_delta():
    """
    Returns the date before now in settings.OFFER_MAX_EXPIRATION_LIMIT days
    """
    now = datetime.datetime.now()
    delta = datetime.timedelta
    return now - delta(days=settings.OFFER_MAX_EXPIRATION_LIMIT)


def pretty_price(value, spacing=' '):
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    return '$' + spacing + locale.format("%d", value, True).replace(',', '.')


def now_plus_min_end_date():
    """Calculates minimum end date for offer creation"""
    today = datetime.date.today()
    delta = datetime.timedelta
    return today + delta(days=settings.OFFER_MIN_EXPIRATION_LIMIT)

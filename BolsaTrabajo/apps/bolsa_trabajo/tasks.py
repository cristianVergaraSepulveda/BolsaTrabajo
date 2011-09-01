# coding: utf-8

from celery.decorators import task

from .models import Offer


@task()
def expire_offers():
    """
    Get all expired open offers and close them
    """
    expired_open_offers = Offer.get_expired()
    for offer in expired_open_offers:
        offer.closed = True
        # TODO: send expiration email to administrator and enterprise owner
        offer.save()

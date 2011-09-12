# coding: utf-8

from celery.task.schedules import crontab
from celery.decorators import periodic_task

from .models import Offer


@periodic_task(run_every=crontab(minute=0, hour=0))
def expire_offers():
    """Get all expired open offers and close them daily at midnight"""
    expired_open_offers = Offer.get_expired()
    for offer in expired_open_offers:
        offer.close_by_task()

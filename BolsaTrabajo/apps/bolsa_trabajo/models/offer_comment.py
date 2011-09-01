#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from . import Student
from . import Offer


class OfferComment(models.Model):
    offer = models.ForeignKey(Offer)
    author = models.ForeignKey(User)
    body = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True)
    has_replies = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    children = property(lambda self: self.offercomment_set.all())

    def set_reply_to_parent(self):
        current_comment = self.parent
        while current_comment:
            current_comment.has_replies = True
            current_comment.save()
            current_comment = current_comment.parent


    def clear(self):
        # Verificar que el autor es estudiante o la empresa original
        if not isinstance(self.author, Student) and self.author != self.offer.enterprise:
            raise ValidationError('Terceras empresas no pueden comentar sobre otras empresas')

    @staticmethod
    def create_from_form(user, offer, form):
        comment = OfferComment()
        comment.offer = offer
        comment.author = user
        comment.body = form.cleaned_data['body']
        if 'parent' in form.cleaned_data:
            comment.parent = form.cleaned_data['parent']
        comment.new_replies = 0
        return comment


    def __unicode__(self):
        return unicode(self.offer) + ' - ' + unicode(self.author)

    class Meta:
        app_label = 'bolsa_trabajo'
        ordering = ('creation_date', )

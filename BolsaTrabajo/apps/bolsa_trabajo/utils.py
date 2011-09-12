# coding: utf-8

import hashlib

from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response

from .models import Enterprise
from .models import Offer
from .models import Student

def user_may_see_student_private_data(user, student):
    if student.profile.approved:
        if not student.profile.block_public_access:
            return True
        if user.is_authenticated() and user.get_profile().may_access_student_private_data(student):
            return True
    return False

def append_account_metadata_to_response(request, template, args={}):
    template_suffix = 'account/base.html'
    if request.user.is_staff:
        template_suffix = 'account/base_superuser.html'
    args['template_suffix'] = template_suffix

    args['pending_enterprise_request_count'] = len(Enterprise.get_pending_requests())
    args['pending_offer_request_count'] = len(Offer.get_pending_requests())
    args['pending_registration_request_count'] = len(Student.get_pending_requests())
    args['pending_offer_status_count'] = len(Offer.get_pendings_feedback_offers())

    return append_user_to_response(request, template, args)


def append_user_to_response(request, template, args={}):
    """Wrapper for the base_generic.html template"""
    args['user'] = request.user
    args['path'] = request.path

    if request.user.is_authenticated() and request.user.profile:
        args['num_notifications'] = len(request.user.profile.get_notifications())
    else:
        args['num_notifications'] = 0

    return render_to_response(template, args, context_instance=RequestContext(request))


def generate_user_digest(username, email):
    return hashlib.sha224(settings.SECRET_KEY + username + email).hexdigest()

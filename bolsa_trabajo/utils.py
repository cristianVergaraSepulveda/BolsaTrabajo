#-*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
import settings
from django.template import Context
from django.core.mail import send_mail
from models import *
from django.contrib.auth.models import User

def append_account_metadata_to_response(request, template, args = {}):
    template_suffix = 'account/base.html'
    if request.user.is_staff:
        template_suffix = 'account/base_superuser.html'
    args['template_suffix'] = template_suffix
    
    args['pending_enterprise_request_count'] = len(Enterprise.get_pending_requests())
    
    return append_user_to_response(request, template, args)

# Wrapper for the base_generic.html template
def append_user_to_response(request, template, args = {}):
    args['user'] = request.user
    args['path'] = request.path
        
    return render_to_response(template, args, context_instance = RequestContext(request))
    
def send_email(user, subject, template, args):
    args['server_name'] = settings.SERVER_NAME 
    args['user'] = user
    body = template.render(Context(args))
    send_mail(subject, body, settings.EMAIL_FULL_ADDRESS, [ user.username + '<' + user.email + '>' ])

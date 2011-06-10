#-*- coding: UTF-8 -*-
import locale
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.template import Context
from django.core.mail import send_mail, EmailMessage
from django.template.loader import get_template
from models import *
from django.contrib.auth.models import User

def append_account_metadata_to_response(request, template, args = {}):
    template_suffix = 'account/base.html'
    if request.user.is_staff:
        template_suffix = 'account/base_superuser.html'
    args['template_suffix'] = template_suffix

    args['pending_enterprise_request_count'] = len(Enterprise.get_pending_requests())
    args['pending_offer_request_count'] = len(Offer.get_pending_requests())

    return append_user_to_response(request, template, args)

# Wrapper for the base_generic.html template
def append_user_to_response(request, template, args = {}):
    args['user'] = request.user
    args['path'] = request.path

    if request.user.is_authenticated() and request.user.profile:
            args['num_notifications'] = len(request.user.profile.get_notifications())
    else:
        args['num_notifications'] = 0

    return render_to_response(template, args, context_instance = RequestContext(request))

def send_contact_message_email(receiver, title, body):
    args = {
        'body': body,
    }
    t = get_template('mails/contact_mail.html')
    content = t.render(Context(args))
    email = EmailMessage('[Bolsa Trabajo CaDCC] ' + title, content, settings.EMAIL_FULL_ADDRESS,
            ['%s <%s>' % (receiver.get_full_name(), receiver.email)], [])
    email.send()

def send_offer_message_email(sender, offer, title, body):
    receiver = offer.enterprise
    args = {
        'offer': offer,
        'body': body,
        'server_name': settings.SERVER_NAME
    }
    t = get_template('mails/personal_mail.html')
    content = t.render(Context(args))
    email = EmailMessage('[Bolsa Trabajo CaDCC] ' + title, content, settings.EMAIL_FULL_ADDRESS,
            ['%s <%s>' % (receiver.get_full_name(), receiver.email)], [],
            headers = {'Reply-To': '%s <%s>' % (sender.get_full_name(), sender.email)})
    email.send()

def send_student_message_email(enterprise, receiver, title, body):
    args = {
        'enterprise': enterprise,
        'body': body,
        'server_name': settings.SERVER_NAME
    }
    t = get_template('mails/personal_student_mail.html')
    content = t.render(Context(args))
    email = EmailMessage('[Bolsa Trabajo CaDCC] ' + title, content, settings.EMAIL_FULL_ADDRESS,
            ['%s <%s>' % (receiver.get_full_name(), receiver.email)], [],
            headers = {'Reply-To': '%s <%s>' % (enterprise.name, enterprise.email)})
    email.send()


def send_email(user, subject, template, args):
    args['server_name'] = settings.SERVER_NAME
    args['user'] = user
    body = template.render(Context(args))
    send_mail(subject, body, settings.EMAIL_FULL_ADDRESS, [ user.username + '<' + user.email + '>' ])

def pretty_price(value, spacing = ' '):
    # Comentado por no funcionar en Windows
    # Este utiliza otros strings de localizacion por ejemplo "enu_us"
    #locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    return '$' + spacing + locale.format("%d", value, True).replace(',', '.')

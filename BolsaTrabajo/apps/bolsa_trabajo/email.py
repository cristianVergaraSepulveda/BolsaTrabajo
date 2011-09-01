# coding: utf-8

from django.conf import settings
from django.template import Context
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import get_template


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
                         headers={'Reply-To': '%s <%s>' % (sender.get_full_name(), sender.email)})
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
                         headers={'Reply-To': '%s <%s>' % (enterprise.name, enterprise.email)})
    email.send()


def send_email(user, subject, template, args):
    args['server_name'] = settings.SERVER_NAME
    args['user'] = user
    body = template.render(Context(args))
    send_mail(subject, body, settings.EMAIL_FULL_ADDRESS, [user.username + '<' + user.email + '>'])

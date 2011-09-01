from django import template
from django.template import Context
from django.template.loader import get_template

register = template.Library()

def tree_comment(comment, user):
    template = get_template('templatetags/offer_comment.html')
    body = template.render(Context({'comment': comment, 'user': user}))
    return body
    
register.filter('tree_comment', tree_comment)

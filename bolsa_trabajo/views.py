#-*- coding: UTF-8 -*-
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from forms import *
from models import *
from utils import *
from django.utils import simplejson

def index(request):
    return append_user_to_response(request, 'index.html', {})
    
def search_tag(request):
    term = request.GET['term']
    tags = Tag.objects.filter(name__istartswith = term)
    response = []
    for tag in tags:
        json_tag = {}
        json_tag['id'] = tag.id
        json_tag['label'] = tag.name
        json_tag['value'] = tag.name
        
        response.append(json_tag)
        
    data = simplejson.dumps(response, indent=4)
    return HttpResponse(data, mimetype='application/javascript')

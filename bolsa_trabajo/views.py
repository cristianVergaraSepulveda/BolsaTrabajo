#-*- coding: UTF-8 -*-
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from forms import *
from models import *
from utils import *

def index(request):
    return append_user_to_response(request, 'index.html', {})

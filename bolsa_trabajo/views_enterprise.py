#-*- coding: UTF-8 -*-
import hashlib
from django.contrib import auth
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from forms import *
from models import *
from utils import *
    
def enterprise_login_required(f):
    def wrap(request, *args, **kwargs):
        uid = request.user.id
        enterprises = Enterprise.objects.filter(pk = uid)
        if enterprises:
            return f(request, *args, **kwargs)
        else:
            url = reverse('bolsa_trabajo.views_account.login')
            path = request.path
            return HttpResponseRedirect(url + '?next=' + path)
    return wrap
    
@enterprise_login_required
def successful_enterprise_registration(request):
    return append_user_to_response(request, 'account/successful_enterprise_response.html')
    
@enterprise_login_required
def offer(request):
    enterprise = Enterprise.objects.get(pk = request.user.id)
    offers = enterprise.offer_set.filter(closed = False)
    return append_user_to_response(request, 'enterprise/offer.html', {
        'offers': offers,
    })
    
@enterprise_login_required
def add_offer(request):
    enterprise = Enterprise.objects.get(pk = request.user.id)
    error = None
    if request.method == 'POST':
        form = OfferForm(request.POST) 
        if form.is_valid():
            offer = Offer.create_from_form(enterprise, form)
            offer.save()
            
            request.flash['message'] = 'Oferta creada exitosamente'
            url = reverse('bolsa_trabajo.views_account.index')
            return HttpResponseRedirect(url)
    else:
        form = OfferForm()
    return append_user_to_response(request, 'enterprise/add_offer.html',{
        'offer_form': form,
        'error': error
    })

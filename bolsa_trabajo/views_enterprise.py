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
    active_offers = enterprise.offer_set.filter(closed = False)
    inactive_offers = enterprise.offer_set.filter(closed = True)
    for inactive_offer in inactive_offers:
        contracts = Contract.objects.filter(application__message__offer = inactive_offer)
        if inactive_offer.available_slots != 0 and len(contracts) == inactive_offer.available_slots:
            inactive_offer.motive = 'Totalidad de cupos rellenos'
        else:
            inactive_offer.motive = 'Cerrada manualmente'
    return append_user_to_response(request, 'enterprise/offer.html', {
        'active_offers': active_offers,
        'inactive_offers': inactive_offers,
    })
    
@enterprise_login_required
def offer_details(request, offer_id):
    offer = Offer.objects.get(pk = offer_id)
    enterprise = Enterprise.objects.get(pk = request.user.id)
    if offer.enterprise != enterprise:
        url = reverse('bolsa_trabajo.views_enterprise.offer')
        return HttpResponseRedirect(url)
        
    return append_user_to_response(request, 'enterprise/offer_details.html',{
        'offer': offer
    })
    
@enterprise_login_required
def edit_offer(request, offer_id):
    offer = Offer.objects.get(pk = offer_id)
    enterprise = Enterprise.objects.get(pk = request.user.id)
    if offer.closed or offer.enterprise != enterprise:
        url = reverse('bolsa_trabajo.views_enterprise.offer')
        return HttpResponseRedirect(url)

    if request.method == 'POST':
        form = OfferForm(request.POST) 
        if form.is_valid():
            offer.load_from_form(form)
            offer.save()
            
            request.flash['message'] = 'Oferta editada exitosamente'
            url = reverse('bolsa_trabajo.views_enterprise.offer_details', args = [offer.id])
            return HttpResponseRedirect(url)
    else:
        form = OfferForm.create_from_offer(offer)
        
    return append_user_to_response(request, 'enterprise/edit_offer.html',{
        'offer_form': form,
        'offer': offer
    })
    
@enterprise_login_required
def close_offer(request, offer_id):
    offer = Offer.objects.get(pk = offer_id)
    enterprise = Enterprise.objects.get(pk = request.user.id)
    if offer.closed or offer.enterprise != enterprise:
        url = reverse('bolsa_trabajo.views_account.index')
        return HttpResponseRedirect(url)

    offer.closed = True
    offer.save()
    request.flash['message'] = 'Oferta cerrada exitosamente'
    
    url = reverse('bolsa_trabajo.views_enterprise.offer')
    return HttpResponseRedirect(url)

    
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
    


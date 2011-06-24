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

    offers = enterprise.offer_set.all()
    pending_offers = []
    active_offers = []
    closed_offers = []

    for offer in offers:
        if not offer.validated:
            pending_offers.append(offer)
        elif not offer.closed:
            active_offers.append(offer)
        else:
            closed_offers.append(offer)

    return append_user_to_response(request, 'enterprise/offer.html', {
        'pending_offers': pending_offers,
        'active_offers': active_offers,
        'closed_offers': closed_offers,
    })

@enterprise_login_required
def offer_details(request, offer_id):
    offer = Offer.objects.get(pk = offer_id)
    enterprise = Enterprise.objects.get(pk = request.user.id)
    if offer.enterprise != enterprise:
        url = reverse('bolsa_trabajo.views_enterprise.offer')
        return HttpResponseRedirect(url)

    form = None

    if offer.closed:
        if request.method == 'POST':
            form = OfferStatusForm(request.POST)
            if form.is_valid():
                offer.change_status_from_form(form)
                offer.save()

                request.flash['message'] = 'Feedback editado exitosamente'
                url = reverse('bolsa_trabajo.views_enterprise.offer')
                return HttpResponseRedirect(url)
        else:
            form = OfferStatusForm.create_from_offer(offer)

    return append_user_to_response(request, 'enterprise/offer_details.html',{
        'offer_form': form,
        'offer': offer
    })

@enterprise_login_required
def edit_offer(request, offer_id):
    offer = Offer.objects.get(pk = offer_id)
    enterprise = Enterprise.objects.get(pk = request.user.id)


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

            UserProfile.notify_staff_of_new_offer()

            request.flash['message'] = 'Oferta propuesta exitosamente, por favor espere a que un encargado la valide'
            url = reverse('bolsa_trabajo.views_account.index')
            return HttpResponseRedirect(url)
    else:
        form = OfferForm()

    return append_user_to_response(request, 'enterprise/add_offer.html',{
        'offer_form': form,
        'error': error
    })

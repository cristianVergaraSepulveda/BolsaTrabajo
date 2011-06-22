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

def staff_login_required(f):
    def wrap(request, *args, **kwargs):
        if request.user.is_staff:
            return f(request, *args, **kwargs)
        else:
            url = reverse('bolsa_trabajo.views_account.login')
            path = request.path
            return HttpResponseRedirect(url + '?next=' + path)

    return wrap

@staff_login_required
def pending_enterprise_request(request):
    return append_account_metadata_to_response(request, 'staff/pending_enterprise_request.html', {
        'pending_requests': Enterprise.get_pending_requests()
    })

@staff_login_required
def pending_enterprise_request_details(request, request_id):
    try:
        enterprise = Enterprise.objects.get(pk = request_id)
        if enterprise.profile.approved:
            raise Exception
        return append_account_metadata_to_response(request, 'staff/pending_enterprise_request_details.html', {
        'enterprise': enterprise
    })
    except Exception, e:
        print str(e)
        raise Exception
        url = reverse('bolsa_trabajo.views_account.index')
        return HttpResponseRedirect(url)

@staff_login_required
def accept_pending_enterprise_request(request, request_id):
    try:
        enterprise = Enterprise.objects.get(pk = request_id)
        if enterprise.profile.approved:
            raise Exception
        enterprise.profile.approved = True
        enterprise.profile.save()
        #enterprise.save()
        enterprise.notify_acceptance()
        request.flash['message'] = 'Empresa aceptada exitosamente'
        url = reverse('bolsa_trabajo.views_account.pending_enterprise_request')
    except:
        url = reverse('bolsa_trabajo.views_account.index')
    return HttpResponseRedirect(url)

@staff_login_required
def reject_pending_enterprise_request(request, request_id):
    try:
        enterprise = Enterprise.objects.get(pk = request_id)
        #if enterprise.is_active:
        if enterprise.profile.approved:
            raise Exception
        enterprise.delete()
        enterprise.notify_rejection()
        request.flash['message'] = 'Solicitud rechazada exitosamente'
        url = reverse('bolsa_trabajo.views_account.pending_enterprise_request')
    except:
        url = reverse('bolsa_trabajo.views_account.index')
    return HttpResponseRedirect(url)

@staff_login_required
def pending_offer_request(request):
    return append_account_metadata_to_response(request, 'staff/pending_offer_request.html', {
        'pending_requests': Offer.get_pending_requests()
    })

@staff_login_required
def pending_offer_request_details(request, request_id):
    try:
        offer = Offer.objects.get(pk = request_id)
        if offer.validated:
            raise Exception
        return append_account_metadata_to_response(request, 'staff/pending_offer_request_details.html', {
        'offer': offer,
        'pending_status': len(Offer.objects.filter(enterprise=offer.enterprise.id).filter(status=None).filter(closed=True))
    })
    except Exception, e:
        print str(e)
        raise Exception
        url = reverse('bolsa_trabajo.views_account.index')
        return HttpResponseRedirect(url)

@staff_login_required
def accept_pending_offer_request(request, request_id):
    try:
        offer = Offer.objects.get(pk = request_id)
        if offer.validated:
            raise Exception
        offer.validated = True
        offer.save()
        offer.notify_acceptance()
        request.flash['message'] = 'Oferta aceptada exitosamente'
        url = reverse('bolsa_trabajo.views_account.pending_offer_request')
    except:
        url = reverse('bolsa_trabajo.views_account.index')
    return HttpResponseRedirect(url)

@staff_login_required
def reject_pending_offer_request(request, request_id):
    try:
        offer = Offer.objects.get(pk = request_id)
        if offer.validated:
            raise Exception
        offer.delete()
        offer.notify_rejection()
        request.flash['message'] = 'Solicitud rechazada exitosamente'
        url = reverse('bolsa_trabajo.views_account.pending_offer_request')
    except:
        url = reverse('bolsa_trabajo.views_account.index')
    return HttpResponseRedirect(url)


@staff_login_required
def new_enterprise(request):
    error = None
    if request.method == 'POST':
        form = EnterpriseRegisterForm(request.POST)
        if form.is_valid():
            enterprise = Enterprise.create_from_form(form)
            #enterprise.is_active = True
            try:
                enterprise.save()

                enterprise.profile.validated_email = True
                enterprise.profile.approved = True
                enterprise.profile.save()

                request.flash['message'] = 'Empresa creada exitosamente'
                url = reverse('bolsa_trabajo.views_account.index')
                return HttpResponseRedirect(url)
            except ValidationError, e:
                error = 'El nombre de usuario ya está tomado'
            except Exception, e:
                error = 'Error desconocido'
    else:
        form = EnterpriseRegisterForm()
    return append_user_to_response(request, 'staff/new_enterprise.html',{
        'register_form': form,
        'error': error
    })

@staff_login_required
def closed_offers(request, request_id):
    try:
        enterprise = Enterprise.objects.get(pk = request_id)
        offers = enterprise.offer_set.all()
        closed_offers = []
        for offer in offers:
            if offer.closed:
                closed_offers.append(offer)
        return append_user_to_response(request, 'staff/closed_offers.html',{
            'closed_offers': closed_offers,
            'enterprise': enterprise
        })

    except Exception, e:
        print str(e)
        raise Exception
        url = reverse('bolsa_trabajo.views_account.index')
        return HttpResponseRedirect(url)


@staff_login_required
def change_offer_status(request, offer_id):
    offer = Offer.objects.get(pk = offer_id)

    if not offer.closed:
        url = reverse('bolsa_trabajo.views_staff.closed_offers', args = [offer.enterprise.id])
        return HttpResponseRedirect(url)

    if request.method == 'POST':
        form = OfferStatusForm(request.POST)
        if form.is_valid():
            offer.change_status_from_form(form)
            offer.save()

            request.flash['message'] = 'Feedback editado exitosamente'
            url = reverse('bolsa_trabajo.views_staff.closed_offers', args = [offer.enterprise.id])
            return HttpResponseRedirect(url)
    else:
        form = OfferStatusForm.create_from_offer(offer)

    return append_user_to_response(request, 'staff/change_offer_status.html',{
        'offer_form': form,
        'offer': offer
    })

@staff_login_required
def all_closed_offers(request):
    try:
        #closed_offers = Offer.objects.filter(status=None).filter(closed=True).values('enterprise').annotate(total=Sum('pk'))
        closed_offers = Offer.objects.values('enterprise').annotate(Count('closed'))
        return append_account_metadata_to_response(request, 'staff/all_closed_offers.html', {
        'closed_offers': closed_offers
    })
    except Exception, e:
        print str(e)
        raise Exception
        url = reverse('bolsa_trabajo.views_account.index')
        return HttpResponseRedirect(url)
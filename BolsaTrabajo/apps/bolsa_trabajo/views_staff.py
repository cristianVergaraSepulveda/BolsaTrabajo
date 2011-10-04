#-*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect

from .forms import *
from .utils import *


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
        enterprise = Enterprise.objects.get(pk=request_id)
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
        enterprise = Enterprise.objects.get(pk=request_id)
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
        enterprise = Enterprise.objects.get(pk=request_id)
        #if enterprise.is_active:
        if enterprise.profile.approved:
            raise Exception
        enterprise.notify_rejection()
        enterprise.delete()
        request.flash['message'] = 'Solicitud rechazada exitosamente'
        url = reverse('bolsa_trabajo.views_account.pending_enterprise_request')
    except:
        url = reverse('bolsa_trabajo.views_account.index')
    return HttpResponseRedirect(url)


@staff_login_required
def pending_registration_request(request):
    return append_account_metadata_to_response(request, 'staff/pending_registration_request.html', {
        'pending_requests': Student.get_pending_requests()
    })


@staff_login_required
def pending_registration_request_details(request, request_id):
    try:
        student = Student.objects.get(pk=request_id)
        if student.profile.approved:
            raise Exception
        return append_account_metadata_to_response(request, 'staff/pending_registration_request_details.html', {
            'student': student
        })
    except Exception, e:
        print str(e)
        raise Exception
        url = reverse('bolsa_trabajo.views_account.index')
        return HttpResponseRedirect(url)


@staff_login_required
def accept_pending_registration_request(request, request_id):
    try:
        student = Student.objects.get(pk=request_id)
        if student.profile.approved:
            raise Exception
        student.profile.approved = True
        student.profile.save()
        #student.save()
        student.notify_acceptance()
        request.flash['message'] = 'Registro aceptado exitosamente'
        url = reverse('bolsa_trabajo.views_account.pending_registration_request')
    except:
        url = reverse('bolsa_trabajo.views_account.index')
    return HttpResponseRedirect(url)


@staff_login_required
def reject_pending_registration_request(request, request_id):
    try:
        student = Student.objects.get(pk=request_id)
        #if registration.is_active:
        if student.profile.approved:
            raise Exception
        student.notify_rejection()
        student.delete()
        request.flash['message'] = 'Solicitud rechazada exitosamente'
        url = reverse('bolsa_trabajo.views_account.pending_registration_request')
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
    offer = Offer.objects.get(pk = request_id)
    if not offer.is_pending():
        return HttpResponseRedirect(reverse('bolsa_trabajo.views_account.index'))
    return append_account_metadata_to_response(request, 'staff/pending_offer_request_details.html', {
        'offer': offer,
    })



@staff_login_required
def accept_pending_offer_request(request, request_id):
    offer = Offer.objects.get(pk = request_id)
    if not offer.is_pending():
        return HttpResponseRedirect(reverse('bolsa_trabajo.views_account.index'))
    offer.open()
    offer.save()
    offer.notify_acceptance()
    request.flash['message'] = 'Oferta aceptada exitosamente'
    url = reverse('bolsa_trabajo.views_staff.pending_offer_request')
    return HttpResponseRedirect(url)


@staff_login_required
def reject_pending_offer_request(request, request_id):
    offer = Offer.objects.get(pk = request_id)
    if offer.is_open():
        return HttpResponseRedirect(reverse('bolsa_trabajo.views_account.index'))
    offer.notify_rejection()
    offer.delete()
    request.flash['message'] = 'Solicitud rechazada exitosamente'
    url = reverse('bolsa_trabajo.views_staff.pending_offer_request')
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
    return append_account_metadata_to_response(request, 'staff/new_enterprise.html', {
        'register_form': form,
        'error': error
    })


@staff_login_required
def closed_offers(request, request_id):
    try:
        enterprise = Enterprise.objects.get(pk=request_id)
        offers = enterprise.offer_set.all()
        closed_offers = []
        for offer in offers:
            if offer.is_closed():
                closed_offers.append(offer)

        return append_account_metadata_to_response(request, 'staff/closed_offers.html', {
            'closed_offers': closed_offers,
            'enterprise': enterprise,
            'pending_requests': Enterprise.get_pending_requests()
        })

    except Exception, e:
        print str(e)
        raise Exception
        url = reverse('bolsa_trabajo.views_account.index')
        return HttpResponseRedirect(url)


@staff_login_required
def change_offer_status(request, offer_id):
    offer = Offer.objects.get(pk = offer_id)
    if not offer.is_closed():
        url = reverse('bolsa_trabajo.views_staff.closed_offers', args = [offer.enterprise.id])
        return HttpResponseRedirect(url)

    if request.method == 'POST':
        form = OfferStatusForm(request.POST)
        if form.is_valid():
            offer.change_status_from_form(form)
            offer.save()

            request.flash['message'] = 'Feedback editado exitosamente'
            url = reverse('bolsa_trabajo.views_staff.closed_offers', args=[offer.enterprise.id])
            return HttpResponseRedirect(url)
    else:
        form = OfferStatusForm.create_from_offer(offer)

    return append_account_metadata_to_response(request, 'staff/change_offer_status.html', {
        'offer_form': form,
        'offer': offer,
        'pending_requests': Enterprise.get_pending_requests()
    })


@staff_login_required
def all_closed_offers(request):
    try:
        closed_offers = Offer.get_pendings_feedback_offers()
        enterprises = Enterprise.objects.all()
        enterprises_offers = {}
        for enterprise in enterprises:
            enterprises_offers[enterprise.name] = [0, enterprise.id]

        for closed_offer in closed_offers:
            enterprises_offers[closed_offer.enterprise.name][0] += 1

        return append_account_metadata_to_response(request, 'staff/all_closed_offers.html', {
            'enterprises_offers': enterprises_offers
        })
    except Exception, e:
        print str(e)
        raise Exception
        url = reverse('bolsa_trabajo.views_account.index')
        return HttpResponseRedirect(url)


@staff_login_required
def concreted_offers(request):
    try:
        concreted_offers = Offer.objects.exclude(status=1).exclude(status=4).exclude(status=5)
        not_concreted_offers = Offer.objects.exclude(status=2).exclude(status=3)

        enterprises = Enterprise.objects.all()
        enterprises_offers = {}

        for enterprise in enterprises:
            enterprises_offers[enterprise.name] = [0, 0]

        for concreted_offer in concreted_offers:
            enterprises_offers[concreted_offer.enterprise.name][0] += 1

        for not_concreted_offer in not_concreted_offers:
            enterprises_offers[not_concreted_offer.enterprise.name][1] += 1

        return append_account_metadata_to_response(request, 'staff/stats.html', {
            'enterprises_offers': enterprises_offers,
            'number_concreted_offers': len(concreted_offers),
            'number_not_concreted_offers': len(not_concreted_offers)
        })
    except Exception, e:
        print str(e)
        raise Exception
        url = reverse('bolsa_trabajo.views_account.index')
        return HttpResponseRedirect(url)

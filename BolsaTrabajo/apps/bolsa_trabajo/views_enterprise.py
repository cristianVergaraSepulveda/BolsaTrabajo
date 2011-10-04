#-*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from models import Enterprise, Offer, UserProfile, Postulation
from forms import OfferStatusForm, OfferForm
from utils import append_user_to_response


def enterprise_login_required(f):
    def wrap(request, *args, **kwargs):
        uid = request.user.id
        enterprises = Enterprise.objects.filter(pk=uid)
        if request.user.is_staff or enterprises:
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
    enterprise = Enterprise.objects.get(pk=request.user.id)
    offers = enterprise.offer_set.all()

    pending_offers = []
    open_offers = []
    closed_offers_with_feedback = []
    closed_offers_without_feedback = []

    for offer in offers:
        if offer.is_pending():
            pending_offers.append(offer)
        elif offer.is_open():
            open_offers.append(offer)
        elif offer.is_closed_with_feedback():
            closed_offers_with_feedback.append(offer)
        else:
            closed_offers_without_feedback.append(offer)

    return append_user_to_response(request, 'enterprise/offer.html', {
        'pending_offers': pending_offers,
        'open_offers': open_offers,
        'closed_offers_with_feedback': closed_offers_with_feedback,
        'closed_offers_without_feedback': closed_offers_without_feedback
        })


@enterprise_login_required
def offer_details(request, offer_id):
    offer = Offer.objects.get(pk=offer_id)
    enterprise = Enterprise.objects.get(pk=request.user.id)
    if offer.enterprise != enterprise:
        request.flash['error_message'] = 'No tiene permisos para ver esta oferta'
        return redirect('bolsa_trabajo.views_enterprise.offer')

    form = None
    if offer.is_closed() and not offer.is_closed_by_admin():
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

    return append_user_to_response(request, 'enterprise/offer_details.html', {
        'offer_form': form,
        'offer': offer,
    })


@enterprise_login_required
def edit_offer(request, offer_id):
    offer = Offer.objects.get(pk=offer_id)
    enterprise = Enterprise.objects.get(pk=request.user.id)

    # check if user has permission to edit this offer
    if offer.enterprise != enterprise:
        request.flash['error_message'] = 'No tiene permisos para editar esta oferta'
        return redirect('bolsa_trabajo.views_enterprise.offer')

    # check first if offer is closed
    if offer.is_closed():
        request.flash['error_message'] = "No puede editar una oferta cerrada"
        return redirect('bolsa_trabajo.views_enterprise.offer')

    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer.load_from_form(form)
            offer.save()

            request.flash['message'] = 'Oferta editada exitosamente'
            url = reverse('bolsa_trabajo.views_enterprise.offer_details', args=[offer.id])
            return HttpResponseRedirect(url)
    else:
        form = OfferForm.create_from_offer(offer)

    close_form = OfferStatusForm()

    return append_user_to_response(request, 'enterprise/edit_offer.html', {
        'offer': offer,
        'offer_form': form,
        'close_form': close_form,
    })


@enterprise_login_required
def close_offer(request, offer_id):
    offer = Offer.objects.get(pk=offer_id)
    if request.user.is_staff:
        enterprise = offer.enterprise
        success_url = reverse('bolsa_trabajo.views.offer_details', args=[offer.id])
    else:
        enterprise = Enterprise.objects.get(pk=request.user.id)
        success_url = reverse('bolsa_trabajo.views_enterprise.offer')

    if offer.enterprise != enterprise:   # unauthorized user
        url = reverse('bolsa_trabajo.views_account.index')
        return HttpResponseRedirect(url)

    if offer.is_closed():  # do nothing in this case
        url = reverse('bolsa_trabajo.views_account.index')
        return HttpResponseRedirect(url)

    if request.user.is_staff:
        offer.close_by_admin()

    elif request.method == 'POST':
        form = OfferStatusForm(request.POST)
        if form.is_valid():
            offer.close(motive=form.cleaned_data['closure_reason'])
        else:
            request.flash['error_message'] = 'Opción de Cierre de Oferta Inválida'
            return HttpResponseRedirect(success_url)

    else:  # GET method, do nothing
        return HttpResponseRedirect(success_url)

    offer.save()
    request.flash['message'] = 'Oferta cerrada exitosamente'

    return HttpResponseRedirect(success_url)


@enterprise_login_required
def add_offer(request):
    enterprise = Enterprise.objects.get(pk=request.user.id)
    error = None

    # If the enterprise has closed offers without feedback
    if enterprise.get_closed_offers_without_feedback():
        request.flash['error_message'] = 'No puede crear nuevas ofertas hasta entregar el feedback de las ya cerradas'
        return HttpResponseRedirect(reverse('bolsa_trabajo.views_enterprise.offer'))

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

    return append_user_to_response(request, 'enterprise/add_offer.html', {
        'offer_form': form,
        'error': error
    })


@enterprise_login_required
def offer_postulations(request, offer_id):
    offer = Offer.objects.get(pk=offer_id)
    if not request.user.is_staff:
        uid = request.user.id
        enterprise = Enterprise.objects.get(pk=uid)
        if offer.enterprise != enterprise:
            request.flash['error_message'] = 'Error de acceso'
            url = reverse('bolsa_trabajo.views_account.index')
            return HttpResponseRedirect(url)
    postulations = offer.postulation_set.filter(status=Postulation.OPEN_POSTULATION)
    return append_user_to_response(request, 'enterprise/offer_postulations.html', {
        'postulations': postulations,
        'offer': offer
    })


@enterprise_login_required
def postulation_details(request, offer_id, postulation_id):
    offer = Offer.objects.get(pk=offer_id)
    postulation = Postulation.objects.get(pk=postulation_id)
    if not request.user.is_staff:
        uid = request.user.id
        enterprise = Enterprise.objects.get(pk=uid)
        if offer.enterprise != enterprise or postulation.offer != offer or postulation.is_closed():
            request.flash['error_message'] = 'Error de acceso'
            url = reverse('bolsa_trabajo.views_account.index')
            return HttpResponseRedirect(url)
    if request.method == 'POST':
        if offer.has_available_slots():
            postulation.close(student_hired=True)
            request.flash['message'] = 'Estudiante contratado exitosamente'
            url = reverse('bolsa_trabajo.views_account.index')
            return HttpResponseRedirect(url)
        else:
            request.flash['error_message'] = 'No hay cupos disponibles para esta oferta'
            url = reverse('bolsa_trabajo.views_account.index')
            return HttpResponseRedirect(url)

    return append_user_to_response(request, 'enterprise/postulation_details.html', {
        'postulation': postulation
    })

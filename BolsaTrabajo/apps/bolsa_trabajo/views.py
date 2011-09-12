#-*- coding: utf-8 -*-

from math import ceil

from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from .forms import *
from .models import *
from .utils import *


def index(request):
    return append_user_to_response(request, 'index.html', {})


def search_tag(request):
    term = request.GET['term']
    tags = Tag.objects.filter(name__istartswith=term)
    response = []
    for tag in tags:
        json_tag = {}
        json_tag['id'] = tag.id
        json_tag['label'] = tag.name
        json_tag['value'] = tag.name

        response.append(json_tag)

    data = simplejson.dumps(response, indent=4)
    return HttpResponse(data, mimetype='application/javascript')


def offer(request):
    form = OfferSearchForm(request.GET)
    offers = Offer.get_from_form(form, request.user.is_authenticated())

    page_number = 1
    if 'page_number' in form.cleaned_data and form.cleaned_data['page_number']:
        page_number = form.cleaned_data['page_number']

    results_per_page = 10
    num_results = len(offers)
    num_pages = ceil(1.0 * num_results / results_per_page)

    offers = offers[((page_number - 1) * results_per_page): (page_number * results_per_page)]

    page_range = range(page_number - 2, page_number + 3)
    page_range = [page for page in page_range if page > 0 and page <= num_pages]

    paging_url = form.generate_paging_url()

    return append_user_to_response(request, 'public/browse_offer.html', {
        'search_form': form,
        'offers': offers,
        'page_number': page_number,
        'page_range': page_range,
        'paging_url': paging_url,
        })


def student(request):
    form = StudentSearchForm(request.GET)
    students = Student.get_from_form(form, request.user.is_authenticated())

    page_number = 1
    if 'page_number' in form.cleaned_data and form.cleaned_data['page_number']:
        page_number = form.cleaned_data['page_number']

    results_per_page = 10
    num_results = len(students)
    num_pages = ceil(1.0 * num_results / results_per_page)

    students = students[((page_number - 1) * results_per_page): (page_number * results_per_page)]

    page_range = range(page_number - 2, page_number + 3)
    page_range = [page for page in page_range if page > 0 and page <= num_pages]

    paging_url = form.generate_paging_url()

    return append_user_to_response(request, 'public/browse_student.html', {
        'search_form': form,
        'students': students,
        'page_number': page_number,
        'page_range': page_range,
        'paging_url': paging_url,
        })


def offer_details(request, offer_id):
    offer = Offer.objects.get(pk=offer_id)
    if not request.user.is_authenticated() and offer.enterprise.profile.block_public_access:
        url = reverse('bolsa_trabajo.views.offer')
        return HttpResponseRedirect(url)

    request.user.can_reply = request.user.profile.can_reply(offer)

    if request.method == 'POST':
        form = OfferCommentForm(request.POST)
        if form.is_valid() and request.user.can_reply:
            offer_comment = OfferComment.create_from_form(request.user, offer, form)
            if offer_comment.parent:
                if offer_comment.parent.offer != offer:
                    url = reverse('bolsa_trabajo.views.offer')
                    return HttpResponseRedirect(url)
            offer_comment.save()
            offer_comment.set_reply_to_parent()

            offer.has_unread_comments = True
            offer.save()

            request.flash['message'] = 'Comentario publicado exitosamente'
            url = reverse('bolsa_trabajo.views.offer_details', args=[offer.id])
            return HttpResponseRedirect(url)
    else:
        form = OfferCommentForm()

    own_comments = OfferComment.objects.filter(author=request.user)
    for comment in own_comments:
        comment.has_replies = False
        comment.save()

    if offer.enterprise.id == request.user.id:
        offer.has_unread_comments = False
        offer.save()

    base_comments = offer.offercomment_set.filter(parent=None)

    return append_search_form_to_response(request, 'public/offer_details.html', {
        'offer': offer,
        'base_comments': base_comments,
        'comment_form': form
    })


def student_details(request, student_id):
    student = Student.objects.get(pk=student_id)
    if not user_may_see_student_private_data(request.user, student):
        url = reverse('bolsa_trabajo.views.student')
        return HttpResponseRedirect(url)
    return append_student_search_form_to_response(request, 'public/student_details.html', {
        'student': student,
        })

def offer_send_message(request, offer_id):
    offer = Offer.objects.get(pk=offer_id)
    #if request.user.is_authenticated() and request.user.profile.is_student() and request.user.is_active:        
    if request.user.is_authenticated() and request.user.profile.is_student() and request.user.profile.approved:
        if request.method == 'POST':
            form = OfferMessageForm(request.POST)
            if form.is_valid() and request.user.profile.approved and request.user.is_authenticated():
                send_offer_message_email(request.user, offer, form.cleaned_data['title'], form.cleaned_data['body'])

                request.flash['message'] = 'Mensaje enviado exitosamente'
                url = reverse('bolsa_trabajo.views.offer_details', args=[offer.id])
                return HttpResponseRedirect(url)
        else:
            form = OfferMessageForm()

        return append_search_form_to_response(request, 'public/offer_send_message.html', {
            'offer': offer,
            'message_form': form
        })
    else:
        url = reverse('bolsa_trabajo.views.offer')
        return HttpResponseRedirect(url)


def student_send_message(request, student_id):
    student = Student.objects.get(pk=student_id)
    #if request.user.is_authenticated() and request.user.profile.is_enterprise() and request.user.is_active:   
    if request.user.is_authenticated() and request.user.profile.is_enterprise() and request.user.profile.approved:
        if request.method == 'POST':
            form = OfferMessageForm(request.POST)
            #if form.is_valid() and request.user.is_active and request.user.is_authenticated():
            if form.is_valid() and request.user.profile.approved and request.user.is_authenticated():
                enterprise = Enterprise.objects.get(pk=request.user.id)
                send_student_message_email(enterprise, student, form.cleaned_data['title'], form.cleaned_data['body'])

                request.flash['message'] = 'Mensaje enviado exitosamente'
                url = reverse('bolsa_trabajo.views.student_details', args=[student.id])
                return HttpResponseRedirect(url)
        else:
            form = OfferMessageForm()

        return append_student_search_form_to_response(request, 'public/student_send_message.html', {
            'student': student,
            'message_form': form
        })
    else:
        url = reverse('bolsa_trabajo.views.student')
        return HttpResponseRedirect(url)


def contact(request):
    if request.method == 'POST':
        form = OfferMessageForm(request.POST)
        if form.is_valid():
            staffs = User.objects.filter(is_staff=True)
            for staff in staffs:
                send_contact_message_email(staff, form.cleaned_data['title'], form.cleaned_data['body'])

            request.flash['message'] = 'Mensaje enviado exitosamente'
            url = reverse('bolsa_trabajo.views.index')
            return HttpResponseRedirect(url)
    else:
        form = OfferMessageForm()

    return append_user_to_response(request, 'public/contact.html', {
        'message_form': form
    })


def enterprise_details(request, enterprise_id):
    enterprise = Enterprise.objects.get(pk=enterprise_id)
    #if not enterprise.is_active:
    if not enterprise.profile.approved:
        url = reverse('bolsa_trabajo.views.index')
        return HttpResponseRedirect(url)
    if not request.user.is_authenticated() and enterprise.profile.block_public_access:
        url = reverse('bolsa_trabajo.views.index')
        return HttpResponseRedirect(url)

    request.user.can_reply = request.user.profile.can_reply_to_enterprise(enterprise)

    if request.method == 'POST':
        form = EnterpriseCommentForm(request.POST)
        if form.is_valid() and request.user.can_reply:
            enterprise_comment = EnterpriseComment.create_from_form(request.user, enterprise, form)
            if enterprise_comment.parent:
                if enterprise_comment.parent.enterprise != enterprise:
                    url = reverse('bolsa_trabajo.views.index')
                    return HttpResponseRedirect(url)
            enterprise_comment.save()
            enterprise_comment.set_reply_to_parent()

            enterprise.has_unread_comments = True
            enterprise.save()

            request.flash['message'] = 'Comentario publicado exitosamente'
            url = reverse('bolsa_trabajo.views.enterprise_details', args=[enterprise.id])
            return HttpResponseRedirect(url)
    else:
        form = EnterpriseCommentForm()

    own_comments = EnterpriseComment.objects.filter(author=request.user)
    for comment in own_comments:
        comment.has_replies = False
        comment.save()

    if enterprise.id == request.user.id:
        enterprise.has_unread_comments = False
        enterprise.save()

    base_comments = enterprise.ent.filter(parent=None)

    return append_search_form_to_response(request, 'public/enterprise_details.html', {
        'enterprise': enterprise,
        'base_comments': base_comments,
        'comment_form': form
    })


def append_search_form_to_response(request, template, args={}):
    args['search_form'] = OfferSearchForm(request.GET)

    return append_user_to_response(request, template, args)


def append_student_search_form_to_response(request, template, args={}):
    args['search_form'] = StudentSearchForm(request.GET)

    return append_user_to_response(request, template, args)

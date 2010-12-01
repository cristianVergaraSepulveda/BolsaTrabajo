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
from math import ceil

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
    
def offer(request):
    form = OfferSearchForm(request.GET)
    offers = Offer.get_from_form(form, request.user.is_authenticated())
    
    page_number = 1
    if 'page_number' in form.cleaned_data and form.cleaned_data['page_number']:
        page_number = form.cleaned_data['page_number']
        
    results_per_page = 10
    num_results = len(offers)
    num_pages = ceil(1.0 * num_results / results_per_page)
    
    offers = offers[((page_number - 1) * results_per_page) : (page_number * results_per_page)]
    
    page_range = range(page_number - 2, page_number + 3)
    page_range = [page for page in page_range if page > 0 and page <= num_pages]
    
    paging_url = form.generate_paging_url()
    
    return append_user_to_response(request, 'public/browse.html', {
        'search_form': form,
        'offers': offers,
        'page_number': page_number,
        'page_range': page_range,
        'paging_url': paging_url,
    }) 
    
def offer_details(request, offer_id):
    offer = Offer.objects.get(pk = offer_id)
    if not request.user.is_authenticated and offer.enterprise.profile.block_public_access:
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
            request.flash['message'] = 'Comentario publicado exitosamente'
            url = reverse('bolsa_trabajo.views.offer_details', args = [offer.id])
            return HttpResponseRedirect(url)
    else:
        form = OfferCommentForm()
        
    base_comments = offer.offercomment_set.filter(parent = None)
    
    return append_search_form_to_response(request, 'public/offer_details.html', {
        'offer': offer,
        'base_comments': base_comments,
        'comment_form': form
    }) 
    
def enterprise_details(request, enterprise_id):
    enterprise = Enterprise.objects.get(pk = enterprise_id)
    if not request.user.is_authenticated and enterprise.profile.block_public_access:
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
            request.flash['message'] = 'Comentario publicado exitosamente'
            url = reverse('bolsa_trabajo.views.enterprise_details', args = [enterprise.id])
            return HttpResponseRedirect(url)
    else:
        form = EnterpriseCommentForm()
        
    base_comments = enterprise.ent.filter(parent = None)
    
    return append_search_form_to_response(request, 'public/enterprise_details.html', {
        'enterprise': enterprise,
        'base_comments': base_comments,
        'comment_form': form
    }) 
    
def append_search_form_to_response(request, template, args = {}):
    args['search_form'] = OfferSearchForm(request.GET)
    
    return append_user_to_response(request, template, args)

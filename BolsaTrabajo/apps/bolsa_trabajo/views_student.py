#-*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from .forms import *
from .models import *
from .utils import *
from .views_account import student_login_required


@student_login_required
def apply_to_offer(request,offer_id):
    offer = Offer.objects.get(pk=offer_id)
    student = Student.objects.get(pk=request.user.id)
    is_already_postulating = student.is_postulating_to(offer)
    error_message = None
    if not student.profile.approved:
        error_message = u'Su perfil aun no ha sido aprobado'
    elif is_already_postulating:
        error_message = u'Usted ya esta postulando a esta oferta'
    elif not student.has_cv:
        error_message = u'Usted debe subir su CV antes de poder postular a una oferta'
    
    if request.method == 'POST':
        if error_message:
            request.flash['error_message'] = error_message
        else:
            postulation = Postulation(offer=offer, student=student)
            postulation.save()
            offer.enterprise.send_postulation_notification_email(postulation)
            request.flash['message'] = u'Su postulación se ha realizado exitosamente'
        url = reverse('bolsa_trabajo.views_account.index')
        return HttpResponseRedirect(url)

    else:
        return append_user_to_response(request, 'student/apply_to_offer.html', {
        'offer':offer,
        'error_message':error_message})

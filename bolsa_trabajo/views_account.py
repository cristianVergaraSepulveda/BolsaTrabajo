#-*- coding: UTF-8 -*-
import hashlib
from django.contrib import auth
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
import os, tempfile, zipfile
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
from forms import *
from models import *
from utils import *

def student_login_required(f):
    def wrap(request, *args, **kwargs):
        uid = request.user.id
        students = Student.objects.filter(pk = uid)
        if students:
            return f(request, *args, **kwargs)
        else:
            url = reverse('bolsa_trabajo.views_account.login')
            path = request.path
            return HttpResponseRedirect(url + '?next=' + path)
    return wrap

@login_required
def notification(request):
    return append_account_metadata_to_response(request, 'account/notifications.html', {
        'notifications': request.user.profile.get_notifications()
    })
    
@login_required
def index(request):
    return append_account_metadata_to_response(request, 'account/index.html')
    
    
@login_required
def public_profile(request):
    if request.user.profile.is_student():
        url = reverse('bolsa_trabajo.views.student_details', args = [request.user.id])
    else:
        url = reverse('bolsa_trabajo.views.enterprise_details', args = [request.user.id])
    
    return HttpResponseRedirect(url)
        
@login_required
def send_register_mail(request):
    next = '/'
    if 'next' in request.GET:
        next = request.GET['next']
    request.user.profile.send_register_mail()
    request.flash['message'] = u'Correo de validación enviado a %s' % request.user.email
    return HttpResponseRedirect(next)

def login(request):
    if 'next' in request.GET:
        next = request.GET['next']
        if next == '/':
            next = '/account/'
    else:
        next = '/account'
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username = username, password = password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(next)
            else:
                request.flash['error_message'] = u'Nombre de usuario o contraseña erróneos'
                return HttpResponseRedirect(request.path)
    else:
        form = LoginForm()
    return append_user_to_response(request, 'account/login.html', {
        'login_form': form
        })
        
def register(request):
    return append_user_to_response(request, 'account/register.html')
    
def register_enterprise(request):
    error = None
    if request.method == 'POST':
        form = EnterpriseRegisterForm(request.POST) 
        if form.is_valid():
            enterprise = Enterprise.create_from_form(form)
            try:
                enterprise.save()
                
                user = auth.authenticate(username = enterprise.username, password = form.cleaned_data['password'])
                if user:
                    auth.login(request, user)
                    user.profile.send_register_mail()
                
                url = reverse('bolsa_trabajo.views_enterprise.successful_enterprise_registration')
                return HttpResponseRedirect(url)
            except ValidationError, e:
                error = 'El nombre de usuario ya está tomado'
            except Exception, e:
                error = 'Error desconocido'
    else:
        form = EnterpriseRegisterForm()
    return append_user_to_response(request, 'account/register_enterprise.html',{
        'register_form': form,
        'error': error
    })

def register_student(request):
    error = None
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST) 
        if form.is_valid():
            student = Student.create_from_form(form)
            try:
                student.save()
                
                user = auth.authenticate(username = student.username, password = form.cleaned_data['password'])
                if user:
                    auth.login(request, user)
                    user.profile.send_register_mail()
                
                url = reverse('bolsa_trabajo.views_account.successful_student_registration')
                return HttpResponseRedirect(url)
            except ValidationError, e:
                error = 'El nombre de usuario ya está tomado'
            except Exception, e:
                error = str(e)
            
    else:
        form = StudentRegisterForm()
    return append_user_to_response(request, 'account/register_student.html',{
        'register_form': form,
        'error': error
    })
    
@student_login_required
def successful_student_registration(request):
    return append_user_to_response(request, 'account/successful_student_response.html')
    
@login_required
def logout(request):
    auth.logout(request)
    request.flash['message'] = 'Sesión cerrada exitosamente'
    next_url = '/'
    if 'next' in request.GET:
        next_url = request.GET['next']
    return HttpResponseRedirect(next_url)
    
@login_required
def validate_email(request):
    try:
        user = request.user
        if user.is_active:
            request.flash['message'] = 'El correo ya está validado'
            url = reverse('bolsa_trabajo.views.index')
            return HttpResponseRedirect(url)
        validation_key = request.GET['validation_key']
        orig_validation_key = hashlib.sha224(settings.SECRET_KEY + user.username + user.email).hexdigest()
        if validation_key != orig_validation_key:
            raise ValidationError('Error en código de validación')

        user.profile.validated_email = True;
        user.profile.save()
        
        if user.profile.is_enterprise():
            UserProfile.notify_staff_of_new_register()
        
        if user.profile.is_student():
            user.is_active = True
            user.save()

        request.flash['message'] = 'Cuenta de correo activada correctamente'
        url = reverse('bolsa_trabajo.views_account.index')
        return HttpResponseRedirect(url)
    except ValidationError, e:
        error = unicode(e)
    except Exception, e:
        error = str(e)
    return append_user_to_response(request, 'account/validate_email.html', {
            'error': error,
        })
        
@login_required
def edit_profile(request):
    if request.user.profile.is_enterprise():
        return edit_enterprise_profile(request)
    else:
        return edit_student_profile(request)
        
def edit_student_profile(request):
    error = None
    student = Student.objects.get(pk = request.user.id)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES) 
        if form.is_valid():
            try:
                student.update_from_form(form)
                student.save()
                student.profile.save()
                
                request.flash['message'] = 'Perfil actualizado exitosamente'
                url = reverse('bolsa_trabajo.views_account.index')
                return HttpResponseRedirect(url)
            except Exception, e:
                error = str(e)
    else:
        form = StudentProfileForm.new_from_student(student)
    return append_user_to_response(request, 'account/edit_student_profile.html',{
        'profile_form': form,
        'error': error,
        'student': student,
    })
    
def edit_enterprise_profile(request):
    error = None
    enterprise = Enterprise.objects.get(pk = request.user.id)
    if request.method == 'POST':
        form = EnterpriseProfileForm(request.POST) 
        if form.is_valid():
            try:
                enterprise.update_from_form(form)
                enterprise.save()
                enterprise.profile.save()
                
                request.flash['message'] = 'Perfil actualizado exitosamente'
                url = reverse('bolsa_trabajo.views_account.index')
                return HttpResponseRedirect(url)
            except Exception, e:
                error = str(e)
    else:
        form = EnterpriseProfileForm.new_from_enterprise(enterprise)
    return append_user_to_response(request, 'account/edit_enterprise_profile.html',{
        'profile_form': form,
        'error': error,
        'enterprise': enterprise,
    })
    
def download_cv(request, student_id):
    try:
        students = Student.objects.filter(pk = student_id)
        if not students:
            raise Exception
        student = students[0]
        if not student.has_cv:
            raise Exception
        if student.profile.block_public_access and not request.user.is_authenticated():
            raise Exception
        filename = settings.PROJECT_ROOT + '/media/cv/%d.pdf' % student.id
        wrapper = FileWrapper(file(filename))
        response = HttpResponse(wrapper, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=curriculum-%s.pdf' % student.get_full_name().replace(' ', '-')
        response['Content-Length'] = os.path.getsize(filename)
        return response
    except:
        return HttpResponseRedirect('/')
        
@student_login_required
def delete_cv(request):
    student = Student.objects.get(pk = request.user.id)
    if student.has_cv:
        student.delete_cv()
        student.save()
        request.flash['message'] = 'Currículum eliminado exitosamente'
    else:
        request.flash['error'] = 'No se tiene currículum'
    url = reverse('bolsa_trabajo.views_account.index')
    return HttpResponseRedirect(url)
    
@login_required
def change_password(request):
    error = None
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if request.user.check_password(form.cleaned_data['old_password']):
                try:
                    request.user.set_password(form.cleaned_data['new_password'])
                    request.user.save()
                    request.flash['message'] = 'Contraseña actualizada exitosamente'
                    url = reverse('bolsa_trabajo.views_account.index')
                    return HttpResponseRedirect(url)
                except Exception, e:
                    error = str(e)
            else:
                error = 'La contraseña original no es correcta'
    else:
        form = ChangePasswordForm()
    return append_user_to_response(request, 'account/change_password.html',{
        'password_form': form,
        'error': error,
    })
    
@login_required
def change_email(request):
    user = request.user
    error = None
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            if user.check_password(form.cleaned_data['password']):
                try:
                    user.email = form.cleaned_data['new_email']
                    if user.profile.is_student():
                        user.is_active = False
                        user.profile.validated_email = False
                        user.profile.send_change_mail_confirmation()
                    user.save()
                    request.flash['message'] = 'E-mail actualizado exitosamente'
                    url = reverse('bolsa_trabajo.views_account.index')
                    return HttpResponseRedirect(url)
                except Exception, e:
                    error = str(e)
            else:
                error = 'La contraseña no es correcta'
    else:
        form = ChangeEmailForm()
    return append_user_to_response(request, 'account/change_email.html',{
        'email_form': form,
        'error': error,
    })

from django.conf.urls.defaults import *

urlpatterns = patterns('bolsa_trabajo.views',
    (r'^search_tag$', 'search_tag'),
    (r'^offer$', 'offer'),
    (r'^$', 'index'))
    
urlpatterns += patterns('bolsa_trabajo.views_account',
    (r'^account/$', 'index'),
    (r'^account/login/$', 'login'),
    (r'^account/logout/$', 'logout'),
    (r'^account/register/$', 'register'),
    (r'^account/register/enterprise/$', 'register_enterprise'),
    (r'^account/register/student/$', 'register_student'),
    (r'^account/successful_student_registration/$', 'successful_student_registration'),
    (r'^account/send_register_mail/$', 'send_register_mail'),
    (r'^account/validate_email/$', 'validate_email'),
    (r'^account/edit_profile/$', 'edit_profile'),
    (r'^account/change_email/$', 'change_email'),
    (r'^account/change_password/$', 'change_password'),
    (r'^account/delete_cv/$', 'delete_cv'),
    (r'^student/(?P<student_id>\d+)/download_cv$', 'download_cv'),
    )
    
urlpatterns += patterns('bolsa_trabajo.views_staff',
    (r'^account/pending_enterprise_request/$', 'pending_enterprise_request'),
    (r'^account/pending_enterprise_request/(?P<request_id>\d+)/$', 'pending_enterprise_request_details'),
    (r'^account/pending_enterprise_request/(?P<request_id>\d+)/accept/$', 'accept_pending_enterprise_request'),
    (r'^account/pending_enterprise_request/(?P<request_id>\d+)/reject/$', 'reject_pending_enterprise_request'),
    (r'^account/new_enterprise/$', 'new_enterprise'),
    )
    
urlpatterns += patterns('bolsa_trabajo.views_enterprise',
    (r'^account/successful_enterprise_registration/$', 'successful_enterprise_registration'),
    (r'^account/offer/$', 'offer'),
    (r'^account/offer/(?P<offer_id>\d+)/$', 'offer_details'),
    (r'^account/offer/(?P<offer_id>\d+)/edit$', 'edit_offer'),
    (r'^account/offer/(?P<offer_id>\d+)/close/$', 'close_offer'),
    (r'^account/offer/add$', 'add_offer'),
    )

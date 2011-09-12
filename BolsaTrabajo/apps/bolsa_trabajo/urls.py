# coding: utf-8

from django.conf.urls.defaults import patterns, url

# generic views

urlpatterns = patterns('bolsa_trabajo.views',
    (r'^search_tag$', 'search_tag'),
    (r'^offer/$', 'offer'),
    (r'^contact/$', 'contact'),
    (r'^offer/(?P<offer_id>\d+)/$', 'offer_details'),
    (r'^offer/(?P<offer_id>\d+)/send_message$', 'offer_send_message'),
    (r'^enterprise/(?P<enterprise_id>\d+)/$', 'enterprise_details'),
    (r'^student/$', 'student'),
    (r'^student/(?P<student_id>\d+)/$', 'student_details'),
    (r'^student/(?P<student_id>\d+)/send_message$', 'student_send_message'),
    (r'^$', 'index'))

# account views

urlpatterns += patterns('bolsa_trabajo.views_account',
    (r'^account/$', 'index'),
    (r'^account/public_profile/$', 'public_profile'),
    (r'^account/notification/$', 'notification'),
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

# staff views

urlpatterns += patterns('bolsa_trabajo.views_staff',
    (r'^account/pending_enterprise_request/$', 'pending_enterprise_request'),
    (r'^account/pending_enterprise_request/(?P<request_id>\d+)/$', 'pending_enterprise_request_details'),
    (r'^account/pending_enterprise_request/(?P<request_id>\d+)/accept/$', 'accept_pending_enterprise_request'),
    (r'^account/pending_enterprise_request/(?P<request_id>\d+)/reject/$', 'reject_pending_enterprise_request'),
    (r'^account/pending_registration_request/$', 'pending_registration_request'),
    (r'^account/pending_registration_request/(?P<request_id>\d+)/$', 'pending_registration_request_details'),
    (r'^account/pending_registration_request/(?P<request_id>\d+)/accept/$', 'accept_pending_registration_request'),
    (r'^account/pending_registration_request/(?P<request_id>\d+)/reject/$', 'reject_pending_registration_request'),
    (r'^account/pending_offer_request/$', 'pending_offer_request'),
    (r'^account/pending_offer_request/(?P<request_id>\d+)/$', 'pending_offer_request_details'),
    (r'^account/pending_offer_request/(?P<request_id>\d+)/accept/$', 'accept_pending_offer_request'),
    (r'^account/pending_offer_request/(?P<request_id>\d+)/reject/$', 'reject_pending_offer_request'),
    (r'^account/new_enterprise/$', 'new_enterprise'),
    (r'^account/all_closed_offers/$', 'all_closed_offers'),
    (r'^account/closed_offers/(?P<request_id>\d+)/$', 'closed_offers'),
    (r'^account/change_offer_status/(?P<offer_id>\d+)/$', 'change_offer_status'),
    (r'^account/statistics/$', 'concreted_offers'),
                        )

# enteprise views

urlpatterns += patterns('bolsa_trabajo.views_enterprise',
    (r'^account/successful_enterprise_registration/$', 'successful_enterprise_registration'),
    (r'^account/offer/$', 'offer'),
    url(r'^account/offer/(?P<offer_id>\d+)/$', 'offer_details', name='enterprise_offer_details'),
    (r'^account/offer/(?P<offer_id>\d+)/edit$', 'edit_offer'),
    url(r'^account/offer/(?P<offer_id>\d+)/close/$', 'close_offer', name='enterprise_close_offer'),
    (r'^account/offer/add$', 'add_offer'),
    (r'^account/offer/(?P<offer_id>\d+)/postulations/$', 'offer_postulations'),
    (r'^account/offer/(?P<offer_id>\d+)/postulations/(?P<postulation_id>\d+)/$', 'postulation_details'),
                        )

# student views

urlpatterns += patterns('bolsa_trabajo.views_student',
    (r'^offer/(?P<offer_id>\d+)/apply_to_offer/$', 'apply_to_offer'),
                        )

# coding: utf-8

from django.conf import settings
from django.contrib import admin
from django.conf.urls.defaults import include, patterns, url


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_project.views.home', name='home'),
    # url(r'^django_project/', include('django_project.foo.urls')),

    # Admin panel and documentation.
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    # Static files.
    #temporal fix while we finish upgrading the templates to django 1.3 syntax
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),

    # django-sentry log viewer.
    (r'^sentry/', include('sentry.web.urls')),

    # Our applications.
    (r'^', include('bolsa_trabajo.urls')),

    # Favicon
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to',
    {'url': settings.MEDIA_URL + 'images/favicon.ico'}),
)

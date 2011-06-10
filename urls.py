from django.conf import settings
from django.contrib import admin
from django.conf.urls.defaults import *

admin.autodiscover()

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    (r'^admin/', include(admin.site.urls)),
	(r'^appsettings/', include('appsettings.urls')),
    (r'^', include('bolsa_trabajo.urls')),
)

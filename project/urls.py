from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
from django.contrib import admin

import competition

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'', include(competition.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url (r'^accounts/login/$', 'django.contrib.auth.views.login',
         {'template_name': 'accounts/login.html'}),
    )

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_ROOT}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

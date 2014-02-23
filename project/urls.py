from django.conf.urls import patterns, url, include
from django.conf import settings
from django.contrib import admin

import competition

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'', include(competition.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url (r'^accounts/login/$',
         'django.contrib.auth.views.login',
         {'template_name': 'accounts/login.html'},
         name='account_login'),
    url (r'^accounts/logout/$',
         'django.contrib.auth.views.logout_then_login',
         name='account_logout'),
    )

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        url(r'^team-qr/(?P<path>.*\.png)$', 'serve',
         {'document_root': settings.QR_DIR}),
        url(r'^static/(?P<path>.*)$', 'serve',
         {'document_root': settings.STATIC_ROOT}),
        url(r'^media/(?P<path>.*)$', 'serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

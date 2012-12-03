from django.conf.urls.defaults import patterns, url, include
from django.conf import settings
from django.contrib import admin

import klaus

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'', include(klaus.urls)),
    url(r'^admin/', include(admin.site.urls)),
    )

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_ROOT}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

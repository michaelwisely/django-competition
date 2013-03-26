from django.conf.urls.defaults import *
from piston.resource import Resource
from competition.api.handlers import CompetitiorHandler

competitor_handler = Resource(CompetitiorHandler)

urlpatterns = patterns('',
   url(r'^competitors/(?P<comp_slug>[\w-]+)/$', competitor_handler, 
        name='api-competition-competitors'),
   url(r'^competitors/(?P<comp_slug>[\w-]+)/free/$', competitor_handler,
        kwargs=dict(free=True), name='api-competition-freeagents'),
   url(r'^competitors/(?P<comp_slug>[\w-]+)/(?P<search>[\w ]+)/$',
        competitor_handler, name='api-competition-competitors-search'),
   url(r'^competitors/(?P<comp_slug>[\w-]+)/free/(?P<search>[\w ]+)/$', 
        competitor_handler, kwargs=dict(free=True), 
        name='api-competition-freeagents-search'),
   url(r'^competitors/(?P<search>[\w ]+)/$', competitor_handler,
        name='api-competitors-search'),
   url(r'^competitors/$', competitor_handler,
        name='api-competitors'),
)

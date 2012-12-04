from django.conf.urls.defaults import patterns, url

from competition.views.competition_views import CompetitionListView
from competition.views.competition_views import CompetitionDetailView
from competition.views.team_views import TeamListView
from competition.views.team_views import TeamDetailView
from competition.views.team_views import TeamCreationView


urlpatterns = patterns(
    "",
    url(r'^competition/$',
        CompetitionListView.as_view(),
        name='competition_list'),
    url(r'^competition/(?P<slug>[\w-]+)/$',
        CompetitionDetailView.as_view(),
        name='competition_detail'),

    url(r'^competition/(?P<comp_slug>[\w-]+)/teams/$',
        TeamListView.as_view(),
        name='team_list'),
    url(r'^competition/(?P<comp_slug>[\w-]+)/team/(?P<slug>[\w-]+)/$',
        TeamDetailView.as_view(),
        name='team_detail'),
    url(r'^competition/(?P<comp_slug>[\w-]+)/team-create/$',
        TeamCreationView.as_view(),
        name='team_create')
    )

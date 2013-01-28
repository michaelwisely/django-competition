from django.conf.urls.defaults import patterns, url

from competition.views.competition_views import CompetitionListView
from competition.views.competition_views import CompetitionDetailView
from competition.views.team_views import TeamListView
from competition.views.team_views import TeamDetailView
from competition.views.team_views import TeamCreationView
from competition.views.team_views import TeamLeaveView
from competition.views.registration_views import RegistrationView
from competition.views.registration_views import UnregisterView


urlpatterns = patterns(
    "",

    # Competition Views
    url(r'^competition/$',
        CompetitionListView.as_view(),
        name='competition_list'),
    url(r'^competition/(?P<comp_slug>[\w-]+)/$',
        CompetitionDetailView.as_view(),
        name='competition_detail'),

    # Team Views
    url(r'^competition/(?P<comp_slug>[\w-]+)/teams/$',
        TeamListView.as_view(),
        name='team_list'),
    url(r'^competition/(?P<comp_slug>[\w-]+)/team/(?P<slug>[\w-]+)/$',
        TeamDetailView.as_view(),
        name='team_detail'),
    url(r'^competition/(?P<comp_slug>[\w-]+)/team-create/$',
        TeamCreationView.as_view(),
        name='team_create'),
    url(r'^competition/(?P<comp_slug>[\w-]+)/team-leave/$',
        TeamLeaveView.as_view(),
        name='team_leave'),

    # Registration Views
    url(r'^competition/(?P<comp_slug>[\w-]+)/register/$',
        RegistrationView.as_view(),
        name='register_for'),

    url(r'^competition/(?P<comp_slug>[\w-]+)/unregister/$',
        UnregisterView.as_view(),
        name='unregister_for')
    )

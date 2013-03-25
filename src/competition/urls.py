from django.conf.urls.defaults import patterns, url, include

from competition.views.competition_views import CompetitionListView
from competition.views.competition_views import CompetitionDetailView
from competition.views.team_views import TeamListView
from competition.views.team_views import FreeAgentListView
from competition.views.team_views import TeamDetailView
from competition.views.team_views import TeamCreationView
from competition.views.team_views import TeamLeaveView
from competition.views.game_views import GameListView
from competition.views.game_views import GameDetailView
from competition.views.invitation_views import InvitationListView
from competition.views.invitation_views import InvitationDetailView
from competition.views.invitation_views import InvitationCreateView
from competition.views.invitation_views import InvitationAcceptView
from competition.views.invitation_views import InvitationDeclineView
from competition.views.registration_views import RegistrationView
from competition.views.registration_views import UnregisterView


urlpatterns = patterns(
    "",

    # API interfaces
    url(r'^competition/api/',
        include('competition.api.urls')),

    # Competition Views
    url(r'^competition/$',
        CompetitionListView.as_view(),
        name='competition_list'),
    url(r'^competition/(?P<comp_slug>[\w-]+)/$',
        CompetitionDetailView.as_view(),
        name='competition_detail'),

    # Team Views
    url(r'^competition/(?P<comp_slug>[\w-]+)/freeagents/$',
        FreeAgentListView.as_view(),
        name='freeagent_list'),
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
        name='unregister_for'),

    # Game Views
    url(r'^competition/(?P<comp_slug>[\w-]+)/games/$',
        GameListView.as_view(),
        name='game_list'),
    url(r'^competition/(?P<comp_slug>[\w-]+)/game/(?P<pk>\d+)/$',
        GameDetailView.as_view(),
        name='game_detail'),

    # Invitation Views
    url(r'^invitations/$',
        InvitationListView.as_view(),
        name='invitation_list'),
    url(r'^invitations/invite/$',
        InvitationCreateView.as_view(),
        name='invitation_create'),
    url(r'^invitations/(?P<pk>\d+)/$',
        InvitationDetailView.as_view(),
        name='invitation_detail'),
    url(r'^invitations/(?P<pk>\d+)/accept$',
        InvitationAcceptView.as_view(),
        name='invitation_accept'),
    url(r'^invitations/(?P<pk>\d+)/decline$',
        InvitationDeclineView.as_view(),
        name='invitation_decline'),
)

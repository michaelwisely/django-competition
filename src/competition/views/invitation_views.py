from django.db.models import Q
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView

from guardian.mixins import PermissionRequiredMixin

from competition.models.team_model import Team
from competition.models.invitation_model import Invitation
from competition.views.mixins import (LoggedInMixin, UserRegisteredMixin,
                                      ConfirmationMixin, RequireOpenMixin,
                                      CheckAllowedMixin)
from competition.forms.invitation_forms import InvitationForm


class InvitationListView(LoggedInMixin, ListView):
    """Lists all teams, provided that the user is logged in"""
    context_object_name = 'invitations'
    template_name = 'competition/invitation/invitation_list.html'
    paginate_by = 10

    def get_queryset(self):
        """Only list invitations for this user"""
        user = self.request.user
        return Invitation.objects.filter(Q(sender=user) | Q(receiver=user))


class InvitationDetailView(LoggedInMixin, DetailView):
    """Show details about a particular team"""
    template_name = 'competition/invitation/invitation_detail.html'
    context_object_name = 'invitation'

    def get_queryset(self):
        """Only show invitations for this user"""
        user = self.request.user
        return Invitation.objects.filter(Q(sender=user) | Q(receiver=user))


class InvitationCreateView(LoggedInMixin,
                           RequireOpenMixin,
                           CreateView):
    """Allow users to create invitations"""
    template_name = 'competition/invitation/invitation_create.html'
    form_class = InvitationForm

    def get_competition(self, request):
        """Called by RequireOpenMixin to determine if the competition
        is open. If it's not open, we throw a 404"""
        return self.get_object().competition

    def get_team(self):
        """If the user provided a 'team' query parameter, look up the
        team. Otherwise return None"""
        try:
            team_id = self.request.GET['team']
            return self.request.user.team_set.get(pk=team_id)
        except (Team.DoesNotExist, KeyError):
            return None

    def get_invitee(self):
        """If the user provided a 'team' query parameter, look up the
        team. Otherwise return None"""
        try:
            invitee_id = self.request.GET['invitee']
            return User.objects.get(pk=invitee_id)
        except (User.DoesNotExist, KeyError):
            return None

    def get_form(self, form_class):
        """Limit the teams that the user can choose from to the teams
        that they are a member of"""
        form = super(InvitationCreateView, self).get_form(form_class)
        form.fields["team"].queryset = self.request.user.team_set
        return form

    def get_form_kwargs(self):
        # Set up keyword arguments for a new Invitation
        invitation_kwargs = (('sender', self.request.user),
                             ('receiver', self.get_invitee()),
                             ('team', self.get_team()))

        # Filter out the values that are None (e.g., if the 'team'
        # query parameter wasn't set, self.get_team() will be None, so
        # we need to filter it out)
        invitation_kwargs = dict((k, v) for (k, v) in invitation_kwargs
                                 if v is not None)

        # Get the default form keyword arguments created by CreateView
        form_kwargs = super(InvitationCreateView, self).get_form_kwargs()

        # Set our instance with our special keyword arguments
        form_kwargs['instance'] = Invitation(**invitation_kwargs)

        return form_kwargs

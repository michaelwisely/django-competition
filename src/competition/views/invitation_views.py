from django.db.models import Q
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.core.urlresolvers import reverse

from competition.models.team_model import Team
from competition.models.invitation_model import Invitation
from competition.views.mixins import (LoggedInMixin, UserRegisteredMixin,
                                      ConfirmationMixin, RequireOpenMixin,
                                      CheckAllowedMixin)
from competition.forms.invitation_forms import InvitationForm

import urllib
import logging


logger = logging.getLogger(__name__)


class InvitationListView(LoggedInMixin, ListView):
    """Lists all teams, provided that the user is logged in"""
    context_object_name = 'invitations'
    template_name = 'competition/invitation/invitation_list.html'
    paginate_by = 10

    def get_queryset(self):
        """Only list invitations for this user"""
        user = self.request.user
        return Invitation.objects.filter(Q(sender=user) | Q(receiver=user))

    def get_context_data(self, **kwargs):
        context = super(InvitationListView, self).get_context_data(**kwargs)
        context['received'] = self.get_queryset().filter(receiver=self.request.user)
        context['sent'] = self.get_queryset().filter(sender=self.request.user)
        return context


class InvitationDetailView(LoggedInMixin, DetailView):
    """Show details about a particular team"""
    template_name = 'competition/invitation/invitation_detail.html'
    context_object_name = 'invitation'

    def get_queryset(self):
        """Only show invitations for this user"""
        user = self.request.user
        return Invitation.objects.filter(Q(sender=user) | Q(receiver=user))

    def get_object(self, queryset=None):
        """When we fetch the invitation, mark it as read"""
        obj = super(InvitationDetailView, self).get_object(queryset)
        if self.request.user == obj.receiver:
            obj.read = True
            obj.save()
        return obj


class InvitationCreateView(LoggedInMixin,
                           CreateView):
    """Allow users to create invitations"""
    template_name = 'competition/invitation/invitation_create.html'
    form_class = InvitationForm

    def get_available_teams(self):
        """Returns a list of competitions that are open for
        registration and team changes"""
        return self.request.user.team_set.filter(competition__is_open=True)

    def get_available_invitees(self):
        """Returns a list of users who can be invited"""
        return User.objects.exclude(pk=self.request.user.pk)

    def get_team(self):
        """If the user provided a 'team' query parameter, look up the
        team. Otherwise return None"""
        try:
            team_id = self.request.GET.get('team')
            if team_id is not None:
                team_id = int(team_id)
                return self.get_available_teams().get(pk=team_id)
            return self.get_available_teams().latest()
        except (Team.DoesNotExist, ValueError):
            return None

    def get_invitee(self):
        """If the user provided a 'invitee' query parameter, look up the
        team. Otherwise return None"""
        try:
            invitee_id = int(self.request.GET['invitee'])
            return self.get_available_invitees().get(pk=invitee_id)
        except (User.DoesNotExist, KeyError, ValueError):
            return None

    def get_form(self, form_class):
        """Limit the teams that the user can choose from to the teams
        that they are a member of"""
        form = super(InvitationCreateView, self).get_form(form_class)
        form.fields["receiver"].queryset = self.get_available_invitees()
        form.fields["team"].queryset = self.get_available_teams()
        form.fields["team"].empty_label = None
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

        # Set our instance with our special keyword arguments and
        # return it
        form_kwargs['instance'] = Invitation(**invitation_kwargs)
        return form_kwargs


class InvitationResponseView(LoggedInMixin,
                             CheckAllowedMixin,
                             ConfirmationMixin):
    """Allows a user to accept or decline an invitation"""
    error_message = 'Cannot accept or decline this invitation at this time'

    def dispatch(self, request, *args, **kwargs):
        """Sets up self.kwargs since we don't have that by default :/"""
        self.kwargs = kwargs
        parent = super(InvitationResponseView, self)
        return parent.dispatch(request, *args, **kwargs)

    def check_if_allowed(self, request):
        # Competition has to be open
        if not self.invitation.team.competition.is_open:
            logger.debug("Can't change invite. Competition closed")
            return False
        # They can't accept or decline again if they've already
        # responded
        if self.invitation.has_response():
            logger.debug("Can't change invite. Already responded")
            return False
        # They can't accept or decline if the message wasn't meant for
        # them.
        if request.user != self.invitation.receiver:
            logger.debug("Can't change invite. Not yours.")
            return False

        # Otherwise we're in good shape.
        return True

    @property
    def invitation(self):
        if not hasattr(self, '_invitation'):
            logger.debug("Fetching invitation")
            invitations = Invitation.objects.select_related()
            self._invitation = get_object_or_404(invitations,
                                                 pk=self.kwargs['pk'])
            logger.debug("Invitation Fetched")
        return self._invitation

    def get_check_box_label(self):
        return "Yes I'm sure"


class InvitationAcceptView(InvitationResponseView):
    """Allows a user to accept an invitation"""
    template_name = 'competition/invitation/invitation_accept.html'

    def get_question(self):
        msg = "Are you sure you want to accept your invitation to join %s?"
        msg += " Joining another team will cause you to automatically leave"
        msg += " any teams that you're on right now."
        return msg % self.invitation.team.name

    def agreed(self):
        competition = self.invitation.team.competition
        invitee = self.invitation.receiver
        if not competition.is_user_registered(invitee):
            # If the user isn't registered, make them register
            msg = "You need to register for %s before you can join a team"
            messages.error(self.request, msg % competition.name)
            url = reverse('register_for',
                          kwargs={'comp_slug': competition.slug})
            query = urllib.urlencode(
                {'next': self.invitation.get_absolute_url()}
            )
            return redirect(url + '?' + query)

        self.invitation.accept()

        msg = "Successfully joined %s" % self.invitation.team.name
        messages.success(self.request, msg)
        return redirect(self.invitation.team)

    def disagreed(self):
        return redirect(self.invitation.team.competition)


class InvitationDeclineView(InvitationResponseView):
    """Allows a user to decline an invitation"""
    template_name = 'competition/invitation/invitation_decline.html'

    def get_question(self):
        msg = "Are you sure you want to decline your invitation to join %s?"
        return msg % self.invitation.team.name

    def agreed(self):
        self.invitation.decline()

        msg = "Successfully declined to join %s" % self.invitation.team.name
        messages.success(self.request, msg)
        return redirect(self.invitation.team.competition)

    def disagreed(self):
        return redirect(self.invitation.team)

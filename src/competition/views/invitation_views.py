from django.db.models import Q
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView

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

    def get_object(self, queryset=None):
        """When we fetch the invitation, mark it as read"""
        obj = super(InvitationDetailView, self).get_object(queryset)
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
                return self.get_available_teams().get(pk=team_id)
            return self.get_available_teams().latest()
        except Team.DoesNotExist:
            return None

    def get_invitee(self):
        """If the user provided a 'team' query parameter, look up the
        team. Otherwise return None"""
        try:
            invitee_id = self.request.GET['invitee']
            return self.get_available_invitees().get(pk=invitee_id)
        except (User.DoesNotExist, KeyError):
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
                             RequireOpenMixin,
                             ConfirmationMixin):
    """Allows a user to accept or decline an invitation"""
    error_message = 'Cannot accept or decline this invitation at this time'

    def check_if_allowed(self, request):
        # Call RequireOpenMixin's check_if_allowed method. If it
        # returns False, bail.
        parent = super(InvitationResponseView, self)
        if parent.check_if_allowed(request) == False:
            return False
        # They can't accept or decline again if they've already
        # responded
        if self.invitation.has_response():
            return False
        # They can't accept or decline if the message wasn't meant for
        # them.
        if request.user != self.invitation.receiver:
            return False

    @property
    def invitation(self):
        if not hasattr(self, '_invitation'):
            self._invitation = get_object_or_404(Invitation,
                                                 pk=self.kwargs['pk'])
        return self._invitation

    def get_check_box_label(self):
        return "Yes I'm sure"


class InvitationAcceptView(InvitationResponseView):
    """Allows a user to accept an invitation"""
    template_name = 'competition/invitation/invitation_accept.html'

    def get_question(self):
        msg = "Are you sure you want to accept your invitation to join %s?"
        return msg % self.invitation.team.name

    def agreed(self):
        self.invitation.accept()

        msg = "Successfully joined %s" % self.invitation.team.name
        messages.success(self.request, msg)
        return redirect(self.invitation.team)

    def disagreed(self):
        return redirect(self.invitation.team.competition)


class InvitationDeclineView(LoggedInMixin, ConfirmationMixin):
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

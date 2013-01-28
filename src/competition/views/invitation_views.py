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
                                      ConfirmationMixin, RequireOpenMixin)
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
                           PermissionRequiredMixin,
                           RequireOpenMixin,
                           CreateView):
    """Allow users to create invitations"""
    template_name = 'competition/invitation/invitation_create.html'
    form_class = InvitationForm
    permission_required = 'competition.change_team'

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.kwargs = kwargs
        return super(InvitationCreateView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        """Called by PermissionRequiredMixin to determine if the user
        has the change_team permission for this team"""
        team = get_object_or_404(self.request.user.team_set,
                                 pk=self.kwargs['team_id'])
        print "Using team: ", team
        print "Perms: ", self.request.user.get_all_permissions()
        return team

    def get_competition(self, request):
        """Called by RequireOpenMixin to determine if the competition
        is open. If it's not open, we throw a 404"""
        return self.get_object().competition

    def on_permission_check_fail(self, request, response, obj=None):
        """Called when the user doesn't have permission to invite a
        user to a team
        """
        raise Http404("User doesn't have permissions to invite to team")

    def get_form_kwargs(self):
        team = self.get_object()
        invitee = get_object_or_404(User, pk=self.kwargs['invitee_id'])

        # If the user's already on team, don't send them an invite.
        if self.team.is_user_on_team(self.invitee):
            msg = "Cannot invite %s to %s. They're already on that team."
            msg = msg % (self.invitee.username, self.team.name)
            messages.info(request, msg)
            return redirect(self.team)        

        kwargs = super(InvitationCreateView, self).get_form_kwargs()
        kwargs['instance'] = Invitation(sender=self.request.user,
                                        receiver=invitee,
                                        team=self.team)
        return kwargs

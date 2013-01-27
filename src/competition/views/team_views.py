from django.db import IntegrityError
from django.http import Http404
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView

from guardian.mixins import PermissionRequiredMixin

from competition.models.team_model import Team
from competition.models.competition_model import Competition
from competition.views.mixins import (CompetitionViewMixin, LoggedInMixin,
                                      UserRegisteredMixin, ConfirmationMixin)
from competition.forms.team_forms import TeamForm


class TeamListView(LoggedInMixin, CompetitionViewMixin, ListView):
    """Lists all teams, provided that the user is logged in"""
    context_object_name = 'teams'
    template_name = 'competition/team/team_list.html'
    paginate_by = 10

    def get_queryset(self):
        """Only list teams participating in self.get_competition()"""
        return Team.objects.filter(competition=self.get_competition())


class TeamDetailView(LoggedInMixin, CompetitionViewMixin, DetailView):
    """Show details about a particular team"""
    template_name = 'competition/team/team_detail.html'
    context_object_name = 'team'

    def get_queryset(self):
        """Only list teams participating in self.get_competition()"""
        return Team.objects.filter(competition=self.get_competition())


class TeamCreationView(UserRegisteredMixin,
                       PermissionRequiredMixin,
                       CreateView):
    """Allow users to create new teams"""
    template_name = 'competition/team/team_create.html'
    form_class = TeamForm
    permission_required = 'competition.create_team'

    def get_object(self):
        """Called by PermissionRequiredMixin to determine if the user
        has the create_team permission for this competition"""
        return self.get_competition()

    def on_permission_check_fail(self, request, response, obj=None):
        """Called when the user doesn't have permission to create a
        new team

        request - the user's request
        response - the automatically generated response redirect to /login/
        obj - the object fetched by get_object
        """
        msg = "Cannot create a new team at this time. "
        msg += "Make sure that you're registered and "
        msg += "that you're not already on a team."
        messages.info(request, msg)

        raise Http404("User is already on a team")

    def form_valid(self, form):
        try:
            team = form.save()
            team.add_team_member(self.request.user)
            return super(TeamCreationView, self).form_valid(form)
        except IntegrityError:
            # If a (competition, team_slug) pair already exists,
            # return the invalid form
            return super(TeamCreationView, self).form_invalid(form)

    def get_form_kwargs(self):
        # Add competition as a keyword argument
        kwargs = super(TeamCreationView, self).get_form_kwargs()
        kwargs['instance'] = Team(competition=self.get_competition())
        return kwargs

from django.views.generic import ListView, DetailView, CreateView
from django.db import IntegrityError
from django.http import Http404
from django.contrib import messages

from competition.models.team_model import Team
from competition.views.mixins import (CompetitionViewMixin, LoggedInMixin,
                                      UserRegisteredMixin)
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


class TeamCreationView(UserRegisteredMixin, CreateView):
    """Allow users to create new teams"""
    template_name = 'competition/team/team_create.html'
    form_class = TeamForm

    def dispatch(self, request, *args, **kwargs):
        try:
            current_teams = Team.objects.filter(
                competition__slug=kwargs['comp_slug'],
                members=request.user
            )

            if current_teams.exists():
                msg = "You're already on a team! You must leave that "
                msg += "team before joining another."
                messages.info(request, msg)
                raise Http404("User is already on a team")
            return super(TeamCreationView, self).dispatch(request, *args, **kwargs)
        except KeyError:
            raise Http404("comp_slug not found in url kwargs")

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

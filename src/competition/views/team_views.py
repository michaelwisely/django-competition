from django.views.generic import ListView, DetailView, CreateView
from django.db import IntegrityError

from competition.models.team_model import Team
from competition.views.mixins import CompetitionViewMixin
from competition.forms.team_forms import TeamForm


class TeamListView(CompetitionViewMixin, ListView):
    """Lists all teams"""
    context_object_name = 'teams'
    template_name = 'competition/team/team_list.html'

    def get_queryset(self):
        """Only list teams participating in self.get_competition()"""
        return Team.objects.filter(competition=self.get_competition())


class TeamDetailView(CompetitionViewMixin, DetailView):
    """Show details about a particular team"""
    template_name = 'competition/team/team_detail.html'

    def get_queryset(self):
        """Only list teams participating in self.get_competition()"""
        return Team.objects.filter(competition=self.get_competition())


class TeamCreationView(CompetitionViewMixin, CreateView):
    """Allow users to create new teams"""
    template_name = 'competition/team/team_create.html'
    form_class = TeamForm

    def form_valid(self, form):
        try:
            team = form.save()
            team.members.add(self.request.user)
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

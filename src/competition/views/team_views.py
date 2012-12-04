from django.views.generic import ListView, DetailView, CreateView

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
        # TODO implement
        # Add requesting user to team 
        # then save
        # then call parent function
        pass
  
    def get_form_kwargs(self):
        # TODO implement
        # Add competition as a keyword argument
        pass

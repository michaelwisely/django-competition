from django.views.generic import ListView, DetailView

from competition.models.competition_model import Competition


class CompetitionListView(ListView):
    """Lists every single competition"""
    context_object_name = 'competitions'
    model = Competition
    template_name = 'competition/competition/competition_list.html'
    paginate_by = 10


class CompetitionDetailView(DetailView):
    """Shows details about a particular competition"""
    context_object_name = 'competition'
    model = Competition
    template_name = 'competition/competition/competition_detail.html'

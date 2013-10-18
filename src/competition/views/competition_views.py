from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist

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
    slug_url_kwarg = 'comp_slug'
    template_name = 'competition/competition/competition_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CompetitionDetailView, self).get_context_data(**kwargs)
        competition = self.object
        user = self.request.user
        context['user_registered'] = competition.is_user_registered(user)
        context['user_team'] = None
        try:
            if not user.is_anonymous():
                context['user_team'] = competition.team_set.get(members=user.pk)
        except ObjectDoesNotExist:
            pass
        return context

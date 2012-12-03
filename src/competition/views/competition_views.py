class CompetitionListView(django.views.generic.list.ListView):
    """Lists every single competition"""
    context_object_name = 'competitions'
    model = Competition
    template_name = 'competition/competition/competition_list.html'


class CompetitionDetailView(django.views.generic.detail.DetailView):
    """Shows details about a particular competition"""
    context_object_name = 'competition'
    model = Competition
    template_name = 'competition/competition/competition_detail.html'

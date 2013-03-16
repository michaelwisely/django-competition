from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from ..models import Game
from .mixins import UserRegisteredMixin, RequireRunningMixin


class GameListView(UserRegisteredMixin,
                   RequireRunningMixin,
                   ListView):
    paginate_by = 25
    context_object_name = 'games'
    template_name = 'competition/game/game_list.html'

    def get_queryset(self):
        team = get_object_or_404(self.request.user.team_set,
                                 competition=self.get_competition())
        return Game.objects.filter(score__team=team)

    def parse_data(self, games):
        fields = set()
        for game in games:
            try:
                fields.add(*game.data['display'].keys())
            except (KeyError, TypeError, AttributeError):
                pass
        return fields

    def get_context_data(self, **kwargs):
        context = super(GameListView, self).get_context_data(**kwargs)
        context['data_fields'] = self.parse_data(context['page_obj'])
        return context

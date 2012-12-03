from django.db import models

from competition.models.game_model import Game
from competition.models.team_model import Team


class Score(models.Model):
    class Meta:
        app_label = 'competition'

    game = models.ForeignKey(Game)
    team = models.ForeignKey(Team)

    score = models.PositiveIntegerField()

from django.db import models
from django.core.exceptions import ValidationError

from competition.models.competition_model import Competition
from competition.models.team_model import Team

import json


class Game(models.Model):
    """Game Model

    To store additional game data, serialize it as a JSON string and
    store it in the extra_data field. If you want the data to be
    available to the user, include it under the "display" key like so:

    {"display": {"location": "place"},
     "referee": "tim"}

    If this information was the extra_data for an object, "location"
    would be displayed for the user, but "referee" would remain hidden.
    """
    class Meta:
        app_label = 'competition'

    competition = models.ForeignKey(Competition)

    created = models.DateTimeField(auto_now_add=True, null=True)
    start_time = models.DateTimeField(null=True,blank=True)
    end_time = models.DateTimeField(null=True,blank=True)
    status = models.CharField(blank=True, max_length=100)

    # Default to JSON null, which gets loaded as None
    extra_data = models.TextField(null=True, default="null")

    def __unicode__(self):
        return "Game #%d" % self.id

    def clean(self):
        if self.start_time and self.end_time and  self.start_time > self.end_time:
            raise ValidationError("Start time is after end time.")
        try:
            if self.extra_data:
                json.loads(self.extra_data)
        except ValueError:
            raise ValidationError("Invalid JSON string.")

    @models.permalink
    def get_absolute_url(self):
        return ('game_detail', (), {'pk': self.pk,
                                    'comp_slug': self.competition.slug})

    @property
    def data(self):
        return json.loads(self.extra_data)

class GameScore(models.Model):
    """
    This is a many to many relation with extra data to score the score of a matchup.
    """
    class Meta:
        app_label = 'competition'

    game = models.ForeignKey(Game)
    team = models.ForeignKey(Team)
    score = models.IntegerField(null=True)
    
    #Default field for extra data for just this match participant.
    extra_data = models.TextField(null=True,default="null")
    
    def __unicode__(self):
        return "Game #{} Team: {} Score {}".format(game.pk,team.name,self.score) 

    def clean(self):
        try:
            if self.extra_dat:
                json.loads(self.extra_data)
            except ValueError:
                raise ValidationError("InvalidJSON string.")
    
    @models.permalink
    def get_absolute_url(self):
        return ('game_detail', (), {'pk': self.game.pk, 
                                    'comp_slug': self.game.competition.slug})

    @property
    def data(self):
        return json.loads(self.extra_data)

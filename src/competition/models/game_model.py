from django.db import models
from django.core.exceptions import ValidationError

from competition.models.competition_model import Competition


class Game(models.Model):
    class Meta:
        app_label = 'competition'

    competition = models.ForeignKey(Competition)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def clean(self):
        if self.start_time > self.end_time:
            raise ValidationError("Start time is after end time.")

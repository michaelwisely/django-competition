from django.db import models
from django.core.exceptions import ValidationError

from competition.models.competition_model import Competition

import json


class Game(models.Model):
    class Meta:
        app_label = 'competition'

    competition = models.ForeignKey(Competition)

    # Default to JSON null, which gets loaded as None
    extra_data = models.TextField(null=True, default="null")

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __unicode__(self):
        return "Game #%d" % self.id

    def clean(self):
        if self.start_time > self.end_time:
            raise ValidationError("Start time is after end time.")
        try:
            if self.extra_data:
                json.loads(self.extra_data)
        except ValueError:
            raise ValidationError("Invalid JSON string.")

    @property
    def data(self):
        return json.loads(self.extra_data)

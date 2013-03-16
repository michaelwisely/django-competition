from django.db import models
from django.core.exceptions import ValidationError

from competition.models.competition_model import Competition

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

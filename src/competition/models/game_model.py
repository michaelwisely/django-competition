"""
g.DoesNotExist             g.end_time                 g.save
g.MultipleObjectsReturned  g.full_clean               g.save_base
g.clean                    g.id                       g.score_set
g.clean_fields             g.is_a_tie                 g.serializable_value
g.competition              g.loser                    g.start_time
g.competition_id           g.objects                  g.unique_error_message
g.date_error_message       g.pk                       g.validate_unique
g.delete                   g.prepare_database_save    g.winner
"""
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from competition.validators import validate_name, positive, greater_than_zero


class Game(models.Model):
    class Meta:
        app_label = 'competition'

    competition = models.ForeignKey(Competition)
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def clean(self):
        #TODO check dates
        pass

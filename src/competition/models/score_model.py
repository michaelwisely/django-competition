"""
s.DoesNotExist             s.game                     s.save_base
s.MultipleObjectsReturned  s.game_id                  s.score
s.clean                    s.id                       s.serializable_value
s.clean_fields             s.objects                  s.team
s.date_error_message       s.pk                       s.team_id
s.delete                   s.prepare_database_save    s.unique_error_message
s.full_clean               s.save                     s.validate_unique
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


class Score(models.Model):
    class Meta:
        app_label = 'competition'

    game = models.ForeignKey(Game)
    team = models.ForeignKey(Team)

    score = models.IntegerField()

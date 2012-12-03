"""
o.DoesNotExist             o.delete                   o.save
o.MultipleObjectsReturned  o.full_clean               o.save_base
o.clean                    o.id                       o.serializable_value
o.clean_fields             o.objects                  o.unique_error_message
o.competition              o.pk                       o.user
o.competition_id           o.prepare_database_save    o.user_id
o.date_error_message       o.role                     o.validate_unique
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


class OrganizerRole(models.Model):
    class Meta:
        app_label = 'competition'

    name = models.CharField(max_length=50, validators=[validate_name])
    description = models.TextField()


class Organizer(models.Model):
    class Meta:
        app_label = 'competition'

    competition = models.ForeignKey(Competition)
    user = models.ForeignKey(User)

    role = models.ManyToManyField(OrganizerRole)


#TODO signals to add users to groups

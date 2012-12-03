from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.contrib.auth.models import User, Group, Permission

from competition.validators import validate_name
from competition.models.competition_model import Competition


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

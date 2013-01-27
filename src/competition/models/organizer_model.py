from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User

from guardian.shortcuts import assign, remove_perm

from competition.validators import validate_name
from competition.models.competition_model import Competition


class OrganizerRole(models.Model):
    class Meta:
        app_label = 'competition'

    name = models.CharField(max_length=50, validators=[validate_name])
    description = models.TextField()

    def __str__(self):
        return self.name


class Organizer(models.Model):
    class Meta:
        app_label = 'competition'

    competition = models.ForeignKey(Competition)
    user = models.ForeignKey(User)

    role = models.ManyToManyField(OrganizerRole)

    def __str__(self):
        return "%s: %s Organizer" % (self.user.username, self.competition.name)


@receiver(post_save, sender=Organizer)
def organizer_post_save(sender, instance, created, **kwargs):
    """Called after an Organizer is saved

    Adds competition-specific permissions to corresponding user
    """
    # If we just made this organizer, grant them organizer permissions
    if created:
        for permission_code in Competition.get_organizer_permissions():
            assign(permission_code, instance.user, instance.competition)


@receiver(pre_delete, sender=Organizer)
def organizer_pre_delete(sender, instance, **kwargs):
    """Called before an Organizer is deleted

    Removes competition-specific permissions from corresponding user
    """
    for permission_code in Competition.get_organizer_permissions():
        remove_perm(permission_code, instance.user, instance.competition)

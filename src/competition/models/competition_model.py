from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from competition.models.avatar_model import Avatar
from competition.validators import validate_name, positive, greater_than_zero


class Competition(models.Model):
    class Meta:
        app_label = 'competition'
        ordering = ['-is_running', '-is_open', '-start_time']

    # Typical info
    name = models.CharField(max_length=50, unique=True,
                            help_text="Name of the competition",
                            validators=[validate_name])
    slug = models.CharField(max_length=50,
                            primary_key=True, blank=True, editable=False,
                            validators=[validate_slug])
    description = models.TextField(help_text="Describe the competition")
    avatar = models.OneToOneField(Avatar, blank=True, null=True)

    # These are the scheduled start and end times for a competition
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # Whether or not the competition is running
    is_open = models.BooleanField(default=False)
    is_running = models.BooleanField(default=False)

    # Questions to ask registering competitors
    questions = models.ManyToManyField("competition.RegistrationQuestion",
                                       blank=True, null=True)

    cost_per_person = models.FloatField(validators=[positive])

    # Team details
    min_num_team_members = models.IntegerField(verbose_name="Minimum number " +
                                               "of players per team",
                                               validators=[greater_than_zero])
    max_num_team_members = models.IntegerField(verbose_name="Maximum number " +
                                               "of players per team",
                                               validators=[greater_than_zero])

    @models.permalink
    def get_absolute_url(self):
        return ('competition_detail', (), {'comp_slug': self.slug})

    def clean(self):
        if self.start_time > self.end_time:
            raise ValidationError("Start time is after end time.")

        if self.min_num_team_members > self.max_num_team_members:
            raise ValidationError("Max number of team members must be " +
                                  " greater than or equal to the min number" +
                                  " of team membeers")

    def __str__(self):
        return self.name

    @property
    def content_type(self):
        return ContentType.objects.get(app_label='competition',
                                       model='competition')

    @property
    def permissions(self):
        return Permission.objects.filter(content_type=self.content_type)

    @property
    def group_name(self):
        return "%s__organizer" % (self.slug, )

    def is_user_registered(self, user):
        """Return true if the given user has an **active**
        registration for this competition, else return false"""
        return self.registration_set.filter(user=user, active=True).exists()


@receiver(pre_save, sender=Competition)
def competition_pre_save(sender, instance, **kwargs):
    """Called before a Competition is saved
    """
    # Set instance's slug if necessary
    if instance.slug == '':
        instance.slug = slugify(instance.name)

    # Create a group with permissions to administer a competition
    if not Group.objects.filter(name=instance.group_name).exists():
        g = Group.objects.create(name=instance.group_name)
        g.permissions = instance.permissions
        g.save()


@receiver(pre_delete, sender=Competition)
def competition_pre_delete(sender, instance, **kwargs):
    """Called before a Competition is deleted
    """
    # Remove the group associated with the Competition being deleted
    try:
        Group.objects.get(name=instance.group_name).delete()
    except Group.DoesNotExist:
        pass

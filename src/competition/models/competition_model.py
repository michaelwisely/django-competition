from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_syncdb
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from competition.validators import (validate_name, non_negative,
                                    greater_than_zero)
from competition.utility import create_thumbnail

import urlparse


class CompetitionManager(models.Manager):

    def user_registered(self, user):
        """Returns competitions that the user is registered for"""
        if user.is_anonymous():
            return []
        return self.filter(registration__user=user.pk,
                           registration__active=True)


class Competition(models.Model):
    class Meta:
        app_label = 'competition'
        ordering = ['-is_running', '-is_open', '-start_time']
        get_latest_by = "created"
        permissions = (
            ("moderate_teams", "Can moderate team names"),
            ("view_registrations", "Can view competitor registrations"),
            ("mark_paid", "Can mark a registration as paid"),
        )

    THUMB_SIZE = getattr(settings, "AVATAR_THUMBNAIL_SIZE", (175, 258))

    PER_TEAM_PAYMENT = 'T'
    PER_PERSON_PAYMENT = 'P'
    PAYMENT_OPTIONS = (
        (PER_TEAM_PAYMENT, 'Per-team Payment'),
        (PER_PERSON_PAYMENT, 'Per-person Payment'),
    )

    # Custom object manager
    objects = CompetitionManager()

    # Typical info
    name = models.CharField(max_length=50, unique=True,
                            help_text="Name of the competition",
                            validators=[validate_name])
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField(help_text="Describe the competition")
    image = models.ImageField(upload_to="competition_images",
                              blank=True, null=True)

    # These are the scheduled start and end times for a competition
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # Whether or not the competition is running
    is_open = models.BooleanField(default=False)
    is_running = models.BooleanField(default=False)

    # Questions to ask registering competitors
    questions = models.ManyToManyField("competition.RegistrationQuestion",
                                       blank=True, null=True)

    payment_option= models.CharField(max_length=1, choices=PAYMENT_OPTIONS,
                                     default=PER_TEAM_PAYMENT)
    cost = models.FloatField(validators=[non_negative])

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
    def _thumbnail_filename(self):
        name_with_extension = os.path.basename(self.image.name)
        name = os.path.splitext(name_with_extension)
        return "t_{}.png".format(name)

    @property
    def thumbnail_path(self):
        directory = os.path.dirname(self.image.path)
        return os.path.join(directory, self._thumbnail_filename)

    @property
    def thumbnail_url(self):
        return urlparse.urljoin(self.image.url, self._thumbnail_filename)

    def is_user_registered(self, user):
        """Return true if the given user has an **active**
        registration for this competition, else return false"""
        if user.is_anonymous():
            return False
        return self.registration_set.filter(user=user.pk, active=True).exists()

    def is_user_organizer(self, user):
        """Return true if the given user is an organizer for this
        competition, else false"""
        if user.is_anonymous():
            return False
        return self.organizer_set.filter(user=user.pk).exists()

    @staticmethod
    def get_organizer_permissions():
        """Returns the permission codes for a competition organizer"""
        return [p[0] for p in Competition._meta.permissions]


@receiver(pre_save, sender=Competition)
def competition_pre_save(sender, instance, update_fields=(), **kwargs):
    """Called before a Competition is saved

    Updates the competition's slug, assigning a unique slug if necessary
    """
    if instance.slug == "":
        slug, i = slugify(instance.name), 1
        while Competition.objects.filter(slug=slug).exists():
            slug = slugify("{0}-{1}".format(instance.name, i))
            i += 1
        instance.slug = slug

    if "image" in update_fields:
        create_thumbnail(instance)




@receiver(post_syncdb, sender=Competition)
def setup_organizer_group(sender, **kwargs):
    comp_content_type = ContentType.objects.get(app_label='competition',
                                                model='competition')
    staff = Group.objects.create(name="Competition Staff")
    perms = Permission.objects.filter(content_type=comp_content_type)
    staff.permissions = perms

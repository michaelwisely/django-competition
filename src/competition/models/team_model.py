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

"""
t.DoesNotExist             t.full_clean               t.pk
t.MultipleObjectsReturned  t.get_absolute_url         t.prepare_database_save
t.clean                    t.get_next_by_created      t.save
t.clean_fields             t.get_previous_by_created  t.save_base
t.competition              t.id                       t.score_set
t.competition_id           t.members                  t.serializable_value
t.created                  t.name                     t.slug
t.date_error_message       t.objects                  t.time_paid
t.delete                   t.paid                     t.unique_error_message
t.eligible_to_win          t.picture                  t.validate_unique
"""


class Team(models.Model):
    class Meta:
        app_label = 'competition'
        unique_together = (('competition', 'slug'),)

    competition = models.ForeignKey(Competition)
    members = models.ManyToMany(User)

    name = models.CharField(max_length=50, validators=[validate_name])
    slug = models.CharField(max_length=50, validators=[validate_slug])

    picture = models.ImageField()
    
    paid = models.BooleanField(default=False)
    time_paid = models.DateTimeField()

    created = models.DateTimeField(auto_add_now=True)
    eligible_to_win = models.BooleanField(default=True)

    @models.permalink
    def get_absolute_url(self):
        kwds = {'comp_slug': self.competition.slug, 'slug': self.slug}
        return ('team_detail', (), kwds)


# TODO slugify receiver

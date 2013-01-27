from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from django.contrib.auth.models import User

from competition.exceptions import TeamException
from competition.models.competition_model import Competition
from competition.models.avatar_model import Avatar
from competition.validators import validate_name, positive, greater_than_zero


class Team(models.Model):
    class Meta:
        app_label = 'competition'
        unique_together = (('competition', 'slug'),)
        ordering = ['name']

    competition = models.ForeignKey(Competition)
    members = models.ManyToManyField(User)

    name = models.CharField(max_length=50, validators=[validate_name])
    slug = models.CharField(max_length=50, validators=[validate_slug])

    avatar = models.OneToOneField(Avatar, blank=True, null=True)

    paid = models.BooleanField(default=False)
    time_paid = models.DateTimeField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    eligible_to_win = models.BooleanField(default=True)

    @models.permalink
    def get_absolute_url(self):
        kwds = {'comp_slug': self.competition.slug, 'slug': self.slug}
        return ('team_detail', (), kwds)

    def __str__(self):
        return "%s" % self.name

    def add_team_member(self, new_user):
        """Adds a user to the calling team

        Raises a TeamException if the team is full

        Removes new_user from any teams they may currently be on for
        the given competition
        """
        # If the team is full, thwo an exception
        if self.members.count() >= self.competition.max_num_team_members:
            raise TeamException("Cannot add new user. Team is already full")
        
        # If new_user is already on a team for this competition, kick them off
        old_teams = Team.objects.filter(competition=self.competition,
                                        members=new_user)
        for team in old_teams:
            team.remove_team_member(new_user)

        # Add the user to this team
        self.members.add(new_user)

    def remove_team_member(self, user):
        """Removes a user from a team

        Deletes the team if they were the last user
        """
        self.members.remove(user)

        if self.members.count() == 0:
            self.delete()

@receiver(pre_save, sender=Team)
def team_pre_save(sender, instance, **kwargs):
    """Called before a Team is saved
    - Sets slug according to name
    """
    instance.slug = slugify(instance.name)

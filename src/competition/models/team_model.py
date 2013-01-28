from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save, m2m_changed
from django.template.defaultfilters import slugify
from django.core.validators import validate_slug
from django.contrib.auth.models import User

from competition.exceptions import TeamException
from competition.models.competition_model import Competition
from competition.models.avatar_model import Avatar
from competition.validators import validate_name
from competition.signals import disable_for_loaddata

import logging
logger = logging.getLogger(__name__)


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
        """
        # If the team is full, thwo an exception
        if self.members.count() >= self.competition.max_num_team_members:
            raise TeamException("Cannot add new user. Team is already full")

        # Add the user to this team
        self.members.add(new_user)

    def remove_team_member(self, user):
        """Removes a user from a team

        Deletes the team if they were the last user
        """
        # Remove them from the team
        self.members.remove(user)

    def is_user_on_team(self, user):
        """Returns true if ``user`` is on the calling team, else
        False"""
        return self.members.filter(pk=user.pk).exists()


@receiver(pre_save, sender=Team)
def team_pre_save(sender, instance, **kwargs):
    """Called before a Team is saved
    - Sets slug according to name
    """
    instance.slug = slugify(instance.name)

@receiver(m2m_changed, sender=Team.members.through)
@disable_for_loaddata
def team_m2m_changed(sender, instance, action, reverse,
                     model, pk_set, **kwargs):
    """Called when a Team's members list is changed"""
    teams = None
    users = None

    # If actions is pre_clear or post_clear, pk_set will be None. If
    # this is the case, just set pk_set to the empty list.
    pk_set = [] if pk_set is None else pk_set

    if reverse:
        # The query is "reversed" if the members are modified by
        # making a call to "user.team_set". In this case, pk_set is a
        # list of Teams, and instance is a User object
        teams = [Team.objects.get(pk=pk) for pk in pk_set]
        users = [instance]
    else:
        # If the query isn't reversed, the members are being modified
        # by making a call to "team.members". In this case, pk_set is
        # a list of Users, and instance is a Team object.
        teams = [instance]
        users = [User.objects.get(pk=pk) for pk in pk_set]

    # If we're adding a new user...
    if action == "pre_add":
        if len(teams) != 1:
            logger.warning("Trying to add user to more than one team")

        for team in teams:
            for user in users:
                # If the team is full, thwo an exception
                if team.members.count() >= team.competition.max_num_team_members:
                    logger.error("%s has too many members on it!", 
                                 team.name)
                # Remove the user from any old teams they might
                # already be on for this competition
                old_teams = user.team_set.filter(competition=team.competition)
                for old_team in old_teams:
                    logger.debug("Removing %s from %s", 
                                 user.username, old_team.name)
                    user.team_set.remove(old_team)

    if action == "post_remove":
        for team in teams:
            for user in users:
                # If there aren't any members left on the team, delete it.
                if team.members.count() == 0:
                    logger.info("%s has no more team members. Deleting it.",
                                team.name)
                    team.delete()


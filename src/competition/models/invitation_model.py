from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.contrib.auth.models import User

from competition.models.competition_model import Competition
from competition.models.team_model import Team


class Invitation(models.Model):
    class Meta:
        app_label = 'competition'
        ordering = ['-sent']

    RESPONSE_CHOICES = (('A', 'Accepted'),
                        ('D', 'Declined'))

    team = models.ForeignKey(Team)

    sender = models.ForeignKey(User, related_name="sent_invitations")
    receiver = models.ForeignKey(User, related_name="received_invitations")

    message = models.TextField()

    sent = models.DateTimeField(auto_now_add=True)

    read = models.BooleanField(default=False)

    response = models.CharField(blank=True, null=True, max_length=2,
                                choices=RESPONSE_CHOICES)
    
    @models.permalink
    def get_absolute_url(self):
        return ('invitation_detail', (), {'id': self.pk})

    def __str__(self):
        return "%s invites %s to join %s" % (self.sender.username, 
                                             self.receiver.username, 
                                             self.team.name)

    def has_response(self):
        """Returns True if the receiver has responded, else False"""
        return self.response is None

    def accept(self):
        """Accepts an invitation to join a team.

        Adds the invitation's recipient to the team. If the team is
        already full, throws an instance of TeamException """
        # If the user's already responded, don't let them respond again
        if self.response is not None:
            return
        self.team.add_team_member(self.receiver)
        self.read = True
        self.response = 'A'     # Accepted
        self.save()

    def decline(self):
        """Declines an invitation to join a team.

        Just marks the invitation as declined"""
        # If the user's already responded, don't let them respond again
        if self.response is not None:
            return
        self.read = True
        self.response = 'D'     # Declined
        self.save()

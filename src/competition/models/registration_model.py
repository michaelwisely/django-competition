from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save

from guardian.shortcuts import assign, remove_perm

from competition.signals import registration_deactivated
from competition.models.competition_model import Competition


class Registration(models.Model):
    class Meta:
        app_label = 'competition'

    user = models.ForeignKey(User)
    competition = models.ForeignKey(Competition)
    signup_date = models.DateTimeField(auto_now_add=True)

    active = models.BooleanField(default=True)

    def __str__(self):
        username = self.user.username
        competition = self.competition.name
        return "%s's registration for %s" % (username, competition)

    def deactivate(self):
        if self.active:
            registration_deactivated.send(sender=self)
            self.active = False
            self.save()


class RegistrationQuestion(models.Model):
    class Meta:
        app_label = 'competition'

    QUESTION_TYPES = (('SC', 'Multiple Choice, Single Answer'),
                      ('MC', 'Multiple Choice, Multiple Answer'),
                      ('SA', 'Short Answer'),
                      ('AB', 'Agreement Check Box'))
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPES)
    question = models.TextField()

    def __str__(self):
        question_type = self.get_question_type_display()
        question = "<blank>" if self.question == '' else self.question
        return '%s Question: "%s": ' % (question_type, question)


class RegistrationQuestionChoice(models.Model):
    class Meta:
        app_label = 'competition'

    question = models.ForeignKey(RegistrationQuestion,
                                 related_name="question_choice_set")
    choice = models.CharField(max_length=100)

    def __str__(self):
        return self.choice

    def clean(self):
        if self.question.question_type not in ('SC', 'MC'):
            msg = "Question choices should only be assigned "
            msg += "to multiple choice questions."
            raise ValidationError(msg)


class RegistrationQuestionResponse(models.Model):
    class Meta:
        app_label = 'competition'

    question = models.ForeignKey(RegistrationQuestion,
                                 related_name="response_set")
    registration = models.ForeignKey(Registration,
                                     related_name="response_set")
    text_response = models.TextField(blank=True)
    choices = models.ManyToManyField(RegistrationQuestionChoice,
                                     null=True, blank=True,
                                     related_name="response_set")
    agreed = models.BooleanField(default=False)

    def __str__(self):
        username = self.registration.user.username
        question = self.question.question
        return "%s's reponse to %s" % (username, question)

    def clean(self):
        if self.question.question_type == 'SC':
            # Skip if the object's still being created
            if self.pk is not None:
                if self.choices.count() != 1:
                    msg = "One choice should be picked for "
                    msg += "single choice response."
                    raise ValidationError(msg)
        if self.question.question_type == 'AB':
            if not self.agreed:
                msg = "Must agree before proceeding"
                raise ValidationError(msg)


@receiver(post_save, sender=Registration)
def registration_post_save(sender, instance, created, raw, **kwargs):
    """Registration has been created and saved

    * Assign user competition.create_team permission if newly created
    """
    # DO NOT modify any other tables if raw is True. raw indicates
    # that Django is setting up the database tables, and no other
    # tables should be modified.
    if created and not raw:
        # If the user just registered, assign their permissions
        assign("create_team", instance.user, instance.competition)

@receiver(registration_deactivated)
def received_registration_deactivated(sender, **kwargs):
    """Registration has been deactivated.

    ``sender`` is the registration being deactivated

    * Revoke the user's permission to create teams
    * Remove the user from any teams they may be on
    """
    # Revoke permissions to create teams
    remove_perm("create_team", sender.user, sender.competition)

    # Remove the user from any teams they're on for this competition
    old_teams = sender.user.team_set.filter(competition=sender.competition)
    for team in old_teams:
        team.members.remove(sender.user)

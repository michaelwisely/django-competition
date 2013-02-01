from django import forms
from django.core.exceptions import ValidationError

from competition.models.invitation_model import Invitation


class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ('team', 'receiver', 'message',)

    def clean(self):
        cleaned_data = super(InvitationForm, self).clean()

        # Make sure the team has invites left
        team = cleaned_data.get('team', None)
        if team is not None:
            if team.num_invites_left() <= 0:
                msg = "Your team has already sent all available team "
                msg += "invitations! Please check your pending invitations."
                raise ValidationError(msg)

        return cleaned_data

    def clean_receiver(self):
        receiver = self.cleaned_data['receiver']
        team = self.cleaned_data.get('team', None)

        # Make sure the user isn't already on the team they're being
        # invited to.
        if team is not None:
            if team.is_user_on_team(receiver):
                msg = "%s is already on your team"
                raise ValidationError(msg % receiver)

        return receiver

    def clean_team(self):
        team = self.cleaned_data['team']

        # Make sure the competition is open for team changes
        if not team.competition.is_open:
            msg = "%s is not currently open for team changes"
            raise ValidationError(msg % team.competition.name)

        return team

from django import forms

from competition.models.invitation_model import Invitation


class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ('team', 'receiver', 'message',)

from django import forms

from competition.models.team_model import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'avatar')

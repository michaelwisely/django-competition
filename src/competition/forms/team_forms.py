from django import forms

from competition.models.team_model import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', )

    def validate_unique(self):
        exclude = self._get_validation_exclusions()
        exclude.remove('competition')

        try:
            self.instance.validate_unique(exclude=exclude)
        except ValidationError, e:
            self._update_errors(e.message_dict)

from django import forms
from django.template.defaultfilters import slugify

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_forms.bootstrap import FormActions

from competition.models.team_model import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                'Create a new team',
                'name',
            ),
            FormActions(
                Submit('submit', 'Submit')
            )
        )
        super(TeamForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        c = self.instance.competition
        s = slugify(self.cleaned_data['name'])
        if Team.objects.filter(competition=c, slug=s).exists():
            msg = "This name is already taken for %s" % c.name
            raise forms.ValidationError(msg)

    def validate_unique(self):
        exclude = self._get_validation_exclusions()
        exclude.remove('competition')

        try:
            self.instance.validate_unique(exclude=exclude)
        except ValidationError, e:
            self._update_errors(e.message_dict)

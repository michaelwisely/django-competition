class TeamForm(django.forms.models.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'picture')
        

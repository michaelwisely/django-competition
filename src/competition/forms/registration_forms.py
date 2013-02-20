from django import forms

def get_form_choices(registration_question):
    """Takes a RegistrationQuestion object and returns a list of
    properly formatted choices for a ChoiceField. Namely, a list of
    tuples.
    """
    raw_choices = registration_question.question_choice_set.all()
    return [(str(rc.id), rc.choice) for rc in raw_choices]


def generate_question_form(registration_question):
    """Generates a form class based on the question being asked
    """
    if registration_question.question_type == 'SC':
        form_choices = get_form_choices(registration_question)

        class SingleChoiceForm(forms.Form):
            sc_response = forms.ChoiceField(
                label=registration_question.question,
                choices=form_choices,
                widget=forms.RadioSelect
            )

        return SingleChoiceForm

    if registration_question.question_type == 'MC':
        form_choices = get_form_choices(registration_question)

        class MultipleChoiceForm(forms.Form):
            mc_response = forms.MultipleChoiceField(
                label=registration_question.question,
                choices=form_choices,
                widget=forms.CheckboxSelectMultiple
                )

        return MultipleChoiceForm

    if registration_question.question_type == 'SA':

        class ShortAnswerForm(forms.Form):
            sa_response = forms.CharField(
                label=registration_question.question,
            )

        return ShortAnswerForm

    if registration_question.question_type == 'AB':

        class AgreementForm(forms.Form):
            ab_response = forms.BooleanField(
                label=registration_question.question,
                required=True
            )

        return AgreementForm

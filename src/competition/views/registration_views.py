from django.views.generic.edit import ProcessFormView
from django.views.generic.base import TemplateResponseMixin
from django.shortcuts import redirect
from django.contrib import messages

from competition.views.mixins import LoggedInMixin, CompetitionViewMixin
from competition.forms.registration_forms import generate_question_form

from competition.models import Registration
from competition.models import RegistrationQuestionChoice as Choice
from competition.models import RegistrationQuestionResponse as Response


class RegistrationView(LoggedInMixin, CompetitionViewMixin,
                       TemplateResponseMixin, ProcessFormView):
    """Allows a user to register to compete"""
    template_name = 'competition/registration/registration_create.html'

    def create_form_classes(self):
        """Generates a list of (question, form) tuples based on the
        current competition
        """
        questions = self.get_competition().questions.select_related().all()
        return [(q, generate_question_form(q)) for q in questions]

    def save_response(self, registration, question, form):
        response = Response.objects.create(question=question, 
                                           registration=registration)

        # If the response was single choice
        if 'sc_response' in form.cleaned_data:
            choice_id = int(form.cleaned_data['sc_response'])
            response.choices.add(Choice.objects.get(pk=choice_id))

        # If the response was multiple choice
        elif 'mc_response' in form.cleaned_data:
            for choice_id in [int(x) for x in form.cleaned_data['mc_response']]:
                response.choices.add(Choice.objects.get(pk=choice_id))

        # If the response was short answer
        elif 'sa_response' in form.cleaned_data:
            response.text_response = form.cleaned_data['sa_response']

        # If the response was a checkbox
        elif 'ab_response' in form.cleaned_data:
            response.agreed = form.cleaned_data['ab_response']

        response.save()

    def get(self, request, *_args, **_kwargs):
        forms = self.create_form_classes()

        # Save a list of the question IDs with the user's session
        request.session['question_ids'] = [q.id for q, _ in forms]

        # Instantiate each of the form classes with its prefix
        forms = [(q, f(prefix=q.id)) for q, f in forms]

        return self.render_to_response({'questions': forms})

    def post(self, request, *_args, **_kwargs):
        forms = self.create_form_classes()
        question_ids = [q.id for q, _ in forms]
        competition = self.get_competition()

        if question_ids != request.session['question_ids']:
            msg = 'The registration form for this competition has changed. '
            msg += 'Please fill out the new forms and resubmit. '
            msg += 'Sorry for the inconvenience!'
            messages.warning(request, msg)

            return redirect('registration_create', 
                            comp_slug=self.get_competition().slug)

        # Create form instances by passing POST data and prefixes
        forms = [(q, f(request.POST, prefix=q.id)) for q, f in forms]
        
        # If all the forms are valid...
        if all(f.is_valid() for _, f in forms):
            registration = Registration.objects.create(user=request.user,
                                                       competition=competition)
            for question, form in forms:
                self.save_response(registration, question, form)
            msg = 'Successfully registered for %s!' % competition.name
            messages.success(request, msg)
            return redirect('competition_list')

        return self.render_to_response({'questions': forms})

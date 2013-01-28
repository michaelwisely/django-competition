from django import forms
from django.http import Http404
from django.views.generic import View
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from competition.models.competition_model import Competition

import logging

logger = logging.getLogger(__name__)


class CompetitionViewMixin(View):
    """A mixin class for adding a competition accessor to the class
    (i.e. self.get_competition()) and adding a competition object to
    the template context, if necessary."""
    def get_competition(self):
        """Returns the competition for the given view.  This requires
        that self.kwargs be set"""
        if not hasattr(self, "_comp"):
            try:
                comp_slug = self.kwargs['comp_slug']
                self._comp = get_object_or_404(Competition, slug=comp_slug)
            except KeyError:
                msg = "Couldn't find comp_slug in kwargs"
                logger.error(msg)
                raise Http404(msg)

        return self._comp

    def dispatch(self, request, *args, **kwargs):
        """Overrides dispatch function to load competition
        information. Raises a Http404 if the competition with slug
        kwargs['comp_slug'] doesn't exist"""
        self.kwargs = kwargs
        self.get_competition()  # Throws Http404 if not found
        parent = super(CompetitionViewMixin, self)
        return parent.dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """Overrides get_context_data to add 'competition' to the
        template context before rendering"""
        context = {'competition': self.get_competition()}
        # Update the context with the parent's context
        parent = super(CompetitionViewMixin, self)
        context.update(parent.get_context_data(*args, **kwargs))
        return context


class LoggedInMixin(View):
    """A mixin class for checking that a user is logged in"""
    redirect_field_name = "next"
    login_url = None

    def login_required(self, dispatch_function):
        """Wraps a function with login_required. Intended to be used
        to wrap a View's dispatch function"""
        return login_required(dispatch_function,
                              redirect_field_name=self.redirect_field_name,
                              login_url=self.login_url)

    def dispatch(self, request, *args, **kwargs):
        """Overrides dispatch by wrapping dispatch with
        login_required"""
        parent = super(LoggedInMixin, self)
        wrapped_function = self.login_required(parent.dispatch)
        return wrapped_function(request, *args, **kwargs)


class UserRegisteredMixin(CompetitionViewMixin, LoggedInMixin):
    """A mixin class for checking that a user is registered for a
    competition"""

    def dispatch(self, request, *args, **kwargs):
        """Overrides dispatch and does the following
           - Checks that a user is authenticated
           - Loads the competition with slug kwargs['comp_slug']
               - Raises a Http404 otherwise
           - Checks that a user is reigstered for the loaded competition
               - Raises a Http404 if they aren't registered"""
        self.kwargs = kwargs    # Needed for get_competition()

        # Causes a 404 if comp_slug kwarg is bad or if the user
        # isn't registered for the corresponding competition
        self.registered_or_404(request)

        # Checks that a user is logged in before returning
        parent = super(UserRegisteredMixin, self)
        wrapped_function = self.login_required(parent.dispatch)
        return wrapped_function(request, *args, **kwargs)

    def registered_or_404(self, request):
        """Checks that the user is registered for the competition
        whose competition slug is kwargs['comp_slug']. If the user is
        not registered, raises Http404"""
        # Causes a 404 if the comp_slug kwarg is bad
        competition = self.get_competition()
        if not competition.is_user_registered(request.user):
            raise Http404("User isn't registered")


class ConfirmationMixin(FormView):
    question = None
    check_box_label = "OK"

    def get_question(self):
        if self.question is None:
            raise Exception("question not set for ConfirmationMixin")
        return self.question

    def get_check_box_label(self):
        return self.check_box_label

    def get_context_data(self, **kwargs):
        kwargs['question'] = self.get_question()
        return super(FormView, self).get_context_data(**kwargs)

    def get_form_class(self):

        class ConfirmationForm(forms.Form):
            confirmed = forms.BooleanField(required=False,
                                           label=self.get_check_box_label())

        return ConfirmationForm

    def form_valid(self, form):
        if form.cleaned_data['confirmed']:
            return self.agreed()
        return self.disagreed()

    def agreed(self):
        """If the user agreed, redirect them to the success url"""
        return redirect(self.get_success_url())

    def disagreed(self):
        """If the user disagreed, redirect them to the success url"""
        return redirect(self.get_success_url())

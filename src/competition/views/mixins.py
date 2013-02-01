from django import forms
from django.http import Http404
from django.contrib import messages
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


class CheckAllowedMixin(View):
    """This mixin throws a 404 if certain conditions are not met.

    At the beginning of the request, this mixin calls
    ``check_if_allowed()`` to see if the user is allowed to view the
    page. If not, it calls ``get_error_message()``, sets an error
    message with level ``self.message_level``, and calls
    ``was_not_allowed`` to determine how to handle the error. The
    default is to throw a 404.

    If the user is allowed to view the page, everything proceeds as
    usual.
    """
    error_message = "You cannot do that"
    message_level = messages.INFO

    def dispatch(self, request, *args, **kwargs):
        if not self.check_if_allowed(request):
            msg = self.get_error_message(request)
            messages.add_message(request, self.message_level, msg)
            return self.was_not_allowed(request)

        parent = super(CheckAllowedMixin, self)
        return parent.dispatch(request, *args, **kwargs)

    def check_if_allowed(self, request):
        """Called to see if a user is allowed to view this page. It
        should return True if they're allowed, and False otherwise.
        """
        raise Exception("check_if_allowed() is not overridden.")

    def get_error_message(self, request):
        """Called to get the user's error message. If not overridden,
        we'll just use ``self.error_message``
        """
        return self.error_message

    def was_not_allowed(self, request):
        """Called if check_if_allowed returned False. If not
        overridden, we'll just throw a 404"""
        raise Http404(self.get_error_message(request))


class RequireRunningMixin(CheckAllowedMixin):
    """This mixin throws a 404 if the current competition is not running
    """
    error_message = "You cannot do that because the competition is not running"

    def check_if_allowed(self, request):
        """Called to see if a user is allowed to view this page.
        """
        # If the competition is running, they're allowed to view it
        return self.get_competition(request).is_running

    def get_competition(self, request):
        """Gets the instance of the competition to check.  

        You could just inherit from CompetitionViewMixin, which
        provides get_competition, just make sure that it's listed
        before RequireRunningMixin when inheriting in the view
        """
        raise Exception("get_competition() not implemented")


class RequireNotRunningMixin(CheckAllowedMixin):
    """This mixin throws a 404 if the current competition is running
    """
    error_message = "You cannot do that because the competition is running"

    def check_if_allowed(self, request):
        """Called to see if a user is allowed to view this page.
        """
        # If the competition is running, they're NOT allowed to view it
        return not self.get_competition(request).is_running

    def get_competition(self, request):
        """Gets the instance of the competition to check.  

        You could just inherit from CompetitionViewMixin, which
        provides get_competition, just make sure that it's listed
        before RequireRunningMixin when inheriting in the view
        """
        raise Exception("get_competition() not implemented")


class RequireOpenMixin(CheckAllowedMixin):
    """This mixin throws a 404 if the current competition is not open
    """
    error_message = "You cannot do that because the competition is not open"

    def check_if_allowed(self, request):
        """Called to see if a user is allowed to view this page.
        """
        # If the competition is open, they're allowed to view it
        return self.get_competition(request).is_open

    def get_competition(self, request):
        """Gets the instance of the competition to check.  

        You could just inherit from CompetitionViewMixin, which
        provides get_competition, just make sure that it's listed
        before RequireRunningMixin when inheriting in the view
        """
        raise Exception("get_competition() not implemented")


class RequireNotOpenMixin(CheckAllowedMixin):
    """This mixin throws a 404 if the current competition is not open
    """
    error_message = "You cannot do that because the competition is open"

    def check_if_allowed(self, request):
        """Called to see if a user is allowed to view this page.
        """
        # If the competition is open, they're NOT allowed to view it
        return not self.get_competition(request).is_open

    def get_competition(self, request):
        """Gets the instance of the competition to check.  

        You could just inherit from CompetitionViewMixin, which
        provides get_competition, just make sure that it's listed
        before RequireRunningMixin when inheriting in the view
        """
        raise Exception("get_competition() not implemented")


class RequireOrganizerMixin(CheckAllowedMixin):
    """This mixin throws a 404 if the user isn't an organizer for this
    competition
    """
    error_message = "Only organizers can do that"

    def check_if_allowed(self, request):
        user = self.get_user(request)
        competition = self.get_competition(request)
        return competition.is_user_organizer(user)

    def get_competition(self, request):
        """Gets the instance of the competition to check.  

        You could just inherit from CompetitionViewMixin, which
        provides get_competition, just make sure that it's listed
        before RequireRunningMixin when inheriting in the view
        """
        raise Exception("get_competition() not implemented")

    def get_user(self, request):
        """Gets the instance of the user to check
        """
        raise Exception("get_user() not implemented")


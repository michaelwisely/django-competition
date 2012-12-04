from django.views.generic import View
from django.shortcuts import get_object_or_404

from competition.models.competition_model import Competition


class CompetitionViewMixin(View):
    """A mixin class for adding a competition accessor to the class
    (i.e. self.get_competition()) and adding a competition object to
    the template context, if necessary."""
    def get_competition(self):
        """Returns the competition for the given view.  This requires
        that self.kwargs be set"""
        comp_slug = self.kwargs['comp_slug']
        return get_object_or_404(Competition, slug=comp_slug)

    def dispatch(self, request, *args, **kwargs):
        """Overrides dispatch function to load competition
        information. Raises a Http404 if the competition with slug
        kwargs['comp_slug'] doesn't exist"""
        self.kwargs = kwargs
        self.get_competition()
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
    def dispatch(self, request, *args, **kwargs):
        """Overrides dispatch by wrapping dispatch with
        login_required"""
        # TODO implement
        pass

    def login_required(self, dispatch_function):
        """Wraps a function with login_required. Intended to be used
        to wrap a View's dispatch function"""
        # TODO implement
        pass


class RequireRegisteredMixin(CompetitionViewMixin):
    """A mixin class for checking that a user is registered for a
    competition"""

    def dispatch(self, request, *args, **kwargs):
        """Overrides dispatch and does the following
           - Checks that a user is authenticated
           - Loads the competition with slug kwargs['comp_slug']
               - Raises a Http404 otherwise
           - Checks that a user is reigstered for the loaded competition
               - Raises a Http404 if they aren't registered"""
        # TODO implement
        pass

    def registered_or_404(self, request):
        """Checks that the user is registered for the competition
        whose competition slug is kwargs['comp_slug']. If the user is
        not registered, raises Http404"""
        # TODO implement
        pass

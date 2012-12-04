from django.views.generic import View


class CompetitionViewMixin(View):
    """A mixin class for adding a competition accessor to the class
    (i.e. self.get_competition()) and adding a competition object to
    the template context, if necessary."""
    def get_competition(self):
        """Returns the competition for the given view.  This requires
        that self.kwargs be set"""
        # TODO implement
        pass

    def dispatch(self, request, *args, **kwargs):
        """Overrides dispatch function to load competition
        information. Raises a Http404 if the competition with slug
        kwargs['comp_slug'] doesn't exist"""
        self.kwargs = kwargs
        self.get_competition()
        parent = super(CometitionViewMixin, self)
        parent.dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """Overrides get_context_data to add 'competition' to the
        template context before rendering"""
        # TODO implement
        pass


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

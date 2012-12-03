class TeamListView(CompetitionViewMixin, ListView):
    """Lists all teams"""
    context_object_name = 'teams'
    template_name = 'competition/team/team_list.html'

    def get_queryset(self):
        """Only lists teams participating in self.get_competition()"""
        # TODO implement
        pass


class TeamDetailView(CompetitionViewMixin, DetailView):
    """Show details about a particular team"""
    template_name = 'competition/team/team_detail.html'

    def get_queryset(self):
        """Make sure team is participating in self.get_competition()"""
        # TODO implement
        pass


class TeamCreationView(CompetitionViewMixin, CreateView):
    """Allow users to create new teams"""
    template_name = 'competition/team/team_create.html'
    form_class = TeamForm

    def form_valid(self, form):
        # TODO implement
        # Add requesting user to team 
        # then save
        # then call parent function
        pass
  
    def get_form_kwargs(self):
        # TODO implement
        # Add competition as a keyword argument
        pass

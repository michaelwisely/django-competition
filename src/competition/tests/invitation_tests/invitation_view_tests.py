from django.core.urlresolvers import reverse

from competition.tests.utils import FancyTestCase
from competition.tests.factories import (UserFactory, CompetitionFactory,
                                         TeamFactory)

from unittest import skip

class InvitationViewsTest(FancyTestCase):

    def setUp(self):
        self.alice = UserFactory.create(username="alice")

        self.space = CompetitionFactory.create(name="Space")
        self.galapagos = CompetitionFactory.create(name="Galapagos")

        self.space_teams = [TeamFactory.create(competition=self.space,
                                               num_members=1)
                            for _ in range(3)]
        self.galapagos_teams = [TeamFactory.create(competition=self.galapagos,
                                                   num_members=1)
                                for _ in range(5)]

    @skip("not implemented")
    def test_invitation_send(self):
        # cannot sent to myself
        # cannot send to users on my team
        # can only send up to max_team_size invitations
        pass

    @skip("not implemented")
    def test_invitation_accept(self):
        # user must be registered for competition
        # causes user to leave any teams they're on
        pass

    @skip("not implemented")
    def test_invitation_reject(self):
        # user stays on team
        # sending team is allowed to send another invite
        pass

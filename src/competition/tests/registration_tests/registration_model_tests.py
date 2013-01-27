from competition.tests.utils import FancyTestCase
from competition.models.team_model import Team
from competition.tests.factories import (UserFactory, CompetitionFactory,
                                         TeamFactory, RegistrationFactory)


class RegistrationModelTest(FancyTestCase):

    def setUp(self):
        self.space = CompetitionFactory.create(name="Space")
        self.galapagos = CompetitionFactory.create(name="Galapagos")

        self.alice = UserFactory.create(username="alice")
        self.bob = UserFactory.create(username="bob")

        # Register Alice and Bob for Space
        self.alice_reg = RegistrationFactory.create(user=self.alice,
                                                    competition=self.space)
        self.bob_reg = RegistrationFactory.create(user=self.bob,
                                                  competition=self.space)

    def test_permissions_set(self):
        """competition.create_team set for registered users"""
        # True, since alice is registered for space
        self.assertTrue(self.alice.has_perm("create_team", self.space))
        # False since she's not registered for galapagos
        self.assertFalse(self.alice.has_perm("create_team", self.galapagos))

    def test_permission_unset(self):
        """competition.create_team revoked for deactivated users"""
        self.alice_reg.deactivate()
        self.assertFalse(self.alice.has_perm("create_team", self.space))

    def test_left_teams(self):
        """deactivation causes users to leave teams"""
        t = TeamFactory.create(competition=self.space, num_members=0)
        t.members.add(self.alice)

        # Alice is definitely on team t
        self.assertEqual(t, self.alice.team_set.get(competition=self.space))
        self.assertEqual(1, self.space.team_set.count())

        self.alice_reg.deactivate()

        # Alice doesn't have a team for space anymore
        alice_space_teams = self.alice.team_set.filter(competition=self.space)
        self.assertFalse(alice_space_teams.exists())
        # And for good measure, space doesn't have any teams anymore
        self.assertEqual(0, self.space.team_set.count())

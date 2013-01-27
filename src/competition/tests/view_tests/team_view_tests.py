from django.core.urlresolvers import reverse

from competition.tests.utils import FancyTestCase
from competition.tests.factories import (UserFactory, CompetitionFactory,
                                         TeamFactory)

from unittest import skip

class TeamViewsTest(FancyTestCase):

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

    def team_num(self, team):
        return int(team.name.replace("Team #", ""))

    def test_authenticated(self):
        """Must be logged in to view teams"""
        kwds = {'comp_slug': self.space.slug}
        teams_url = reverse("team_list", kwargs=kwds)
        response = self.client.get(teams_url)
        self.assertRedirects(response, '/accounts/login/?next=' + teams_url)

        with self.loggedInAs("alice", "123"):
            response = self.client.get(teams_url)
            self.assertEqual(200, response.status_code)

    def test_list_teams(self):
        """List teams for a competition"""
        # Create some more teams
        for _i in range(10):
            TeamFactory.create(competition=self.space, num_members=0)

        with self.loggedInAs("alice", "123"):
            response = self.client.rget('team_list',
                                        kwargs={'comp_slug': self.space.slug})

        objects = response.context['teams']

        for i in range(len(objects) - 1):
            self.assertLess(objects[i].name, objects[i + 1].name)

        # Paginator sanity check
        self.assertTrue(response.context['is_paginated'])

    @skip("not implemented")
    def test_team_detail(self):
        """Check users for team"""
        pass

    @skip("not implemented")
    def test_create_team(self):
        # Must be registered
        # Can't be on more then one team for a competition
        pass

    @skip("not implemented")
    def test_team_deleted(self):
        # When all users leave, team gets deleted
        pass

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

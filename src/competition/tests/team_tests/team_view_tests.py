from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group

from competition.tests.utils import FancyTestCase
from competition.models.team_model import Team
from competition.tests.factories import (UserFactory, CompetitionFactory,
                                         TeamFactory, RegistrationFactory)

from unittest import skip

class TeamViewsTest(FancyTestCase):

    def setUp(self):
        self.space = CompetitionFactory.create(name="Space",
                                               is_open=True)
        self.galapagos = CompetitionFactory.create(name="Galapagos",
                                                   is_open=True)

        self.space_teams = [TeamFactory.create(competition=self.space,
                                               num_members=1)
                            for _ in range(3)]
        self.galapagos_teams = [TeamFactory.create(competition=self.galapagos,
                                                   num_members=1)
                                for _ in range(5)]
        self.alice = UserFactory.create(username="alice")
        self.bob = UserFactory.create(username="bob")
        self.carl = UserFactory.create(username="carl")
        # Register Alice and Bob for Space
        self.alice_reg = RegistrationFactory.create(user=self.alice,
                                                    competition=self.space)
        self.bob_reg = RegistrationFactory.create(user=self.bob,
                                                  competition=self.space)

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

    def test_team_detail(self):
        """Check users for team"""
        team = self.space_teams[1]
        with self.loggedInAs("alice", "123"):
            resp = self.client.get(team.get_absolute_url())
        self.assertEqual(team, resp.context['team'])

    def test_create_team(self):
        """Registered users can create teams"""
        num_teams = Team.objects.all().count()
        url = reverse('team_create', kwargs={'comp_slug': self.space.slug})
        with self.loggedInAs("alice", "123"):
            resp = self.client.get(url)
            self.assertIn('form', resp.context)
            resp = self.client.post(url, follow=True,
                                    data={'name': 'Team Awesome'})
        self.assertEqual(num_teams + 1, Team.objects.all().count())

        team = Team.objects.get(competition=self.space, members=self.alice)
        self.assertRedirects(resp, team.get_absolute_url())
        self.assertEqual(1, team.members.count())
        self.assertEqual('Team Awesome', team.name)
        self.assertEqual('team-awesome', team.slug)  # Make sure slug got set
        self.assertInGroup(self.alice, team.get_group())
        self.assertEqual(1, self.alice.groups.count())

    def test_create_team_unregistered(self):
        """unregistered users cannot create teams"""
        num_teams = Team.objects.all().count()
        url = reverse('team_create', kwargs={'comp_slug': self.space.slug})
        with self.loggedInAs("carl", "123"):
            resp = self.client.get(url)
            self.assert404(resp)

        self.assertEqual(num_teams, Team.objects.all().count())

    def test_create_team_duplicate(self):
        """Users cannot create duplicate teams"""
        num_teams = Team.objects.all().count()
        url = reverse('team_create', kwargs={'comp_slug': self.space.slug})
        with self.loggedInAs("alice", "123"):
            # Alice creates a team
            resp = self.client.post(url, data={'name': 'Team Awesome'})
        with self.loggedInAs("bob", "123"):
            # Bob tries to create a team with the same name
            resp = self.client.post(url, follow=True,
                                    data={'name': 'Team Awesome'})

        # Bob didn't create a new team
        self.assertEqual(num_teams + 1, Team.objects.all().count())
        self.assertFalse(Team.objects.filter(members=self.bob).exists())
        self.assertEqual(0, self.bob.groups.count())

    def test_create_team_registered(self):
        """Must be registered to create a team"""
        self.alice_reg.deactivate()
        url = reverse('team_create', kwargs={'comp_slug': self.space.slug})
        with self.loggedInAs("alice", "123"):
            # Alice creates a team
            resp = self.client.post(url, data={'name': 'Team Awesome'})
        self.assert404(resp)

    def test_cant_be_on_a_team_already(self):
        """Can't create a team if you're already on a team"""
        url = reverse('team_create', kwargs={'comp_slug': self.space.slug})
        with self.loggedInAs("alice", "123"):
            # Alice creates a team
            resp = self.client.post(url, data={'name': 'Team Awesome'})
            # Alice creates another team
            resp = self.client.post(url, data={'name': 'Another Team'})
        self.assert404(resp)

    def test_leave_team(self):
        """Confiming leaving a team causes user to leave team"""
        url = reverse('team_leave', kwargs={'comp_slug': self.space.slug})
        t = TeamFactory.create(competition=self.space, num_members=1)
        t.members.add(self.alice)

        self.assertEqual(2, t.members.count())   # Sanity check
        self.assertInGroup(self.alice, t.get_group())
        self.assertEqual(1, self.alice.groups.count())

        with self.loggedInAs("alice", "123"):
            resp = self.client.get(url)
            self.assertEqual(200, resp.status_code)
            self.assertIn("Are you sure", resp.context['question'])

            resp = self.client.post(url, data={'confirmed': True}, follow=True)
            self.assertRedirects(resp, self.space.get_absolute_url())
            self.assertEqual(1, t.members.count())
            self.assertEqual(0, self.alice.groups.count())

    def test_leave_team_decline(self):
        """Declining leaving a team does nothing"""
        url = reverse('team_leave', kwargs={'comp_slug': self.space.slug})
        t = TeamFactory.create(competition=self.space, num_members=1)
        t.members.add(self.alice)

        self.assertEqual(2, t.members.count())   # Sanity check
        self.assertInGroup(self.alice, t.get_group())

        with self.loggedInAs("alice", "123"):
            resp = self.client.post(url, data={'confirmed': False}, follow=True)
            self.assertRedirects(resp, t.get_absolute_url())
            self.assertEqual(2, t.members.count())
            self.assertInGroup(self.alice, t.get_group())

    def test_leave_team_no_team(self):
        """Users can't leave a team if they're not on a team"""
        url = reverse('team_leave', kwargs={'comp_slug': self.space.slug})
        with self.loggedInAs("alice", "123"):
            resp = self.client.get(url)
            self.assertEqual(404, resp.status_code)

    def test_team_deleted(self):
        """Teams get deleted when everyone leaves"""
        url = reverse('team_leave', kwargs={'comp_slug': self.space.slug})
        t = TeamFactory.create(competition=self.space, num_members=0)
        t.members.add(self.alice)

        # Sanity checks
        self.assertTrue(Team.objects.filter(pk=t.pk).exists())
        self.assertEqual(1, t.members.count())
        self.assertInGroup(self.alice, t.get_group())
        self.assertEqual(1, self.alice.groups.count())

        with self.loggedInAs("alice", "123"):
            resp = self.client.post(url, data={'confirmed': True}, follow=True)
            self.assertRedirects(resp, self.space.get_absolute_url())
            self.assertFalse(Team.objects.filter(pk=t.pk).exists())
            self.assertEqual(0, self.alice.groups.count())
            self.assertEqual(0, Group.objects.filter(name=t.group_name).count())

    def test_create_team_competition_closed(self):
        """Users can't create a team if competition is closed"""
        self.space.is_open = False
        self.space.save()
        url = reverse('team_create', kwargs={'comp_slug': self.space.slug})
        with self.loggedInAs("alice", "123"):
            resp = self.client.get(url)
            self.assertEqual(404, resp.status_code)

    def test_leave_team_competition_closed(self):
        """Users can't leave a team if competition is closed"""
        self.space.is_open = False
        self.space.save()
        url = reverse('team_leave', kwargs={'comp_slug': self.space.slug})
        with self.loggedInAs("alice", "123"):
            resp = self.client.get(url)
            self.assertEqual(404, resp.status_code)

    def test_team_deleted_on_unregister(self):
        """Team gets deleted when the last user unregisters"""
        num_teams = Team.objects.all().count()
        url = reverse('team_create', kwargs={'comp_slug': self.space.slug})
        with self.loggedInAs("alice", "123"):
            resp = self.client.post(url, follow=True,
                                    data={'name': 'Team Awesome'})
        self.assertEqual(num_teams + 1, Team.objects.all().count())
        self.alice_reg.deactivate()  # Deactivate registration
        self.assertEqual(num_teams, Team.objects.all().count())  # one less team

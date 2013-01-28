from django.test import TestCase
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from competition.exceptions import TeamException
from competition.tests.utils import FancyTestCase
from competition.models.team_model import Team
from competition.tests.factories import (UserFactory, CompetitionFactory,
                                         TeamFactory, RegistrationFactory)


class TeamModelTest(FancyTestCase):

    def setUp(self):
        self.space = CompetitionFactory.create(name="Space")
        self.galapagos = CompetitionFactory.create(name="Galapagos")

        self.space_teams = [TeamFactory.create(competition=self.space,
                                               num_members=1)
                            for _ in range(3)]
        self.galapagos_teams = [TeamFactory.create(competition=self.galapagos,
                                                   num_members=1)
                                for _ in range(5)]
        self.alice = UserFactory.create(username="alice")
        self.bob = UserFactory.create(username="bob")

        # Register Alice and Bob for Space
        self.alice_reg = RegistrationFactory.create(user=self.alice,
                                                    competition=self.space)
        self.bob_reg = RegistrationFactory.create(user=self.bob,
                                                  competition=self.space)

    def test_duplicate_names(self):
        """Teams with duplicate names are not ok"""
        TeamFactory.create(name="Team Awesome", competition=self.space)
        with self.assertRaises(IntegrityError):
            TeamFactory.create(name="Team Awesome", competition=self.space)

    def test_slug_set(self):
        """Teams should have their slugs set automatically"""
        t = TeamFactory.create(name="Team Awesome", competition=self.space)
        self.assertEqual("team-awesome", t.slug)

    def test_add_team_member(self):
        """add_team_member method should add one member"""
        t = self.space_teams[0]
        self.assertEqual(1, t.members.count())
        t.add_team_member(self.alice)
        self.assertEqual(2, t.members.count())

    def test_add_team_member_max_team_size(self):
        """add_team_member throws an exception if team is full"""
        t = TeamFactory.create(name="Team Awesome", competition=self.space,
                               num_members=3)
        with self.assertRaises(TeamException):
            t.add_team_member(self.alice)

    def test_add_team_member_remove_from_old_teams(self):
        """add_team_member boots users off old teams"""
        t0 = self.space_teams[0]
        t1 = self.space_teams[1]
        t0.add_team_member(self.alice)
        t1.add_team_member(self.alice)

        self.assertFalse(t0.members.filter(pk=self.alice.pk).exists())
        self.assertTrue(t1.members.filter(pk=self.alice.pk).exists())

    def test_remove_team_member(self):
        """remove_team_member deletes empty teams"""
        t = TeamFactory.create(name="Team Awesome", competition=self.space,
                               num_members=2)
        member1, member2 = t.members.all()[0], t.members.all()[1]

        # Remove member1, team still exists
        t.remove_team_member(member1)
        self.assertTrue(Team.objects.filter(pk=t.pk).exists())
        self.assertFalse(t.members.filter(pk=member1.pk).exists())

        # Remove member 2, team doesn't exist anymore
        t.remove_team_member(member2)
        self.assertFalse(Team.objects.filter(pk=t.pk).exists())

    def test_members_clear(self):
        """team.members.clear() removes permissions"""
        t = TeamFactory.create(name="Team Awesome", competition=self.space,
                               num_members=2)
        members = t.members.all()
        t.members.clear()

        for member in members:
            self.assertFalse(t.is_user_on_team(member))

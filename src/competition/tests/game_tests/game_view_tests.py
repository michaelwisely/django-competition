from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group

from competition.tests.utils import FancyTestCase
from competition.models.game_model import Game
from competition.tests.factories import (UserFactory, CompetitionFactory,
                                         TeamFactory, RegistrationFactory,
                                         GameFactory)

from unittest import skip
import random


class GameViewsTest(FancyTestCase):

    def setUp(self):
        self.space = CompetitionFactory.create(name="Space",
                                               is_running=True)

        self.space_teams = [TeamFactory.create(competition=self.space,
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

        # Add users to teams
        self.space_teams[0].members.add(self.alice)
        self.space_teams[1].members.add(self.bob)

        GameFactory.create(team1=self.space_teams[0],
                           team2=self.space_teams[1],
                           competition=self.space)
        GameFactory.create(team1=self.space_teams[0],
                           team2=self.space_teams[2],
                           competition=self.space)
        for _ in range(20):
            team1, team2 = random.sample(self.space_teams, 2)
            GameFactory.create(team1=team1, team2=team2,
                               competition=self.space)

    def test_authenticated(self):
        """Must be logged in to view games"""
        kwds = {'comp_slug': self.space.slug}
        games_url = reverse("game_list", kwargs=kwds)
        response = self.client.get(games_url)
        self.assert404(response)

        with self.loggedInAs("alice", "123"):
            response = self.client.get(games_url)
            self.assertEqual(200, response.status_code)

    def test_is_running(self):
        """Must be running to view games"""
        kwds = {'comp_slug': self.space.slug}
        games_url = reverse("game_list", kwargs=kwds)
        with self.loggedInAs("alice", "123"):
            response = self.client.get(games_url)
            self.assertEqual(200, response.status_code)

        self.space.is_running = False
        self.space.save()

        # Doesn't work if competition isn't running.
        with self.loggedInAs("alice", "123"):
            response = self.client.get(games_url)
            self.assertEqual(404, response.status_code)

    def test_view_own_games(self):
        """Must view own games"""
        kwds = {'comp_slug': self.space.slug}
        games_url = reverse("game_list", kwargs=kwds)
        with self.loggedInAs("alice", "123"):
            response = self.client.get(games_url)
            self.assertTrue(len(response.context['games']) > 0)
            for game in response.context['games']:
                if self.space_teams[0] != game.team1:
                    self.assertEqual(self.space_teams[0], game.team2)

    def test_view_own_game_details(self):
        """Must view details for own games"""
        # Alice is team1, not-Bob is team2
        games = self.space.game_set.filter(team1=self.space_teams[0],
                                           team2=self.space_teams[2])
        kwds = {'comp_slug': self.space.slug, 'pk': games[0].pk}
        games_url = reverse("game_detail", kwargs=kwds)
        with self.loggedInAs("alice", "123"):
            response = self.client.get(games_url)
            self.assertEqual(200, response.status_code)

        with self.loggedInAs("bob", "123"):
            response = self.client.get(games_url)
            self.assertEqual(404, response.status_code)

    def test_both_teams_view_details(self):
        """Both teams must view details for own games"""
        # Alice is team1, Bob is team2
        games = self.space.game_set.filter(team1=self.space_teams[0],
                                           team2=self.space_teams[1])
        kwds = {'comp_slug': self.space.slug, 'pk': games[0].pk}
        games_url = reverse("game_detail", kwargs=kwds)
        with self.loggedInAs("alice", "123"):
            response = self.client.get(games_url)
            self.assertEqual(200, response.status_code)

        with self.loggedInAs("bob", "123"):
            response = self.client.get(games_url)
            self.assertEqual(200, response.status_code)

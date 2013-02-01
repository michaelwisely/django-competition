from django.core.urlresolvers import reverse

from competition.models.invitation_model import Invitation
from competition.tests.utils import FancyTestCase
from competition.tests.factories import (UserFactory, CompetitionFactory,
                                         TeamFactory)

from unittest import skip


class InvitationViewsTest(FancyTestCase):

    def setUp(self):
        self.alice = UserFactory.create(username="alice")
        self.bob = UserFactory.create(username="bob")
        self.carl = UserFactory.create(username="carl")

        self.space = CompetitionFactory.create(name="Space",
                                               is_open=False)
        self.galapagos = CompetitionFactory.create(name="Galapagos",
                                                   is_open=True)

        self.alice_team = TeamFactory.create(competition=self.galapagos,
                                             num_members=0)
        self.alice_team.add_team_member(self.alice)

        self.bob_team = TeamFactory.create(competition=self.galapagos,
                                           num_members=0)
        self.bob_team.add_team_member(self.bob)

    def test_invitation_send(self):
        """Invitations are sent to users"""
        with self.loggedInAs("alice", "123"):
            resp = self.client.rget('invitation_create')
            self.assertEqual(200, resp.status_code)

            resp = self.client.rpost('invitation_create',
                                     follow=True,
                                     data={'team': self.alice_team.pk,
                                           'receiver': self.carl.pk,
                                           'message': "Hello"})
        invitations = Invitation.objects.all()
        self.assertEqual(1, invitations.count())
        self.assertRedirects(resp, invitations[0].get_absolute_url())

    def test_invitation_with_query_params(self):
        """Invitation is partially filled out with query params"""
        with self.loggedInAs("alice", "123"):
            resp = self.client.rget('invitation_create',
                                    data={'team': self.alice_team.pk,
                                          'invitee': self.carl.pk})
            initial = resp.context['form'].initial
            self.assertEqual(self.carl.pk, initial['receiver'])
            self.assertEqual(self.alice_team.pk, initial['team'])

    def test_default_team_param(self):
        """Invitation uses lastest team as default"""
        with self.loggedInAs("alice", "123"):
            resp = self.client.rget('invitation_create')
            initial = resp.context['form'].initial
            self.assertEqual(self.alice.team_set.latest().pk, initial['team'])

    def test_invalid_invitee_param(self):
        """Invitation has invalid invitee query param"""
        with self.loggedInAs("alice", "123"):
            resp = self.client.rget('invitation_create',
                                    data={'invitee': -12})
            initial = resp.context['form'].initial
            self.assertIsNone(initial['receiver'])

    def test_invalid_team_param(self):
        """Invitation has invalid team query param"""
        with self.loggedInAs("alice", "123"):
            resp = self.client.rget('invitation_create',
                                    data={'team': -12})
            initial = resp.context['form'].initial
            self.assertIsNone(initial['team'])

    def test_cannot_send_to_me(self):
        """Can't invite myself"""
        with self.loggedInAs("alice", "123"):
            resp = self.client.rpost('invitation_create',
                                     follow=True,
                                     data={'team': self.alice_team.pk,
                                           'receiver': self.alice.pk,
                                           'message': "Hello"})
        self.assertIn('receiver', resp.context['form'].errors)
        self.assertEqual(0, Invitation.objects.all().count())

    def test_cannot_invite_to_another_team(self):
        """Can't invite user to a team that's not mine"""
        with self.loggedInAs("alice", "123"):
            resp = self.client.rpost('invitation_create',
                                     follow=True,
                                     data={'team': self.bob_team.pk,
                                           'receiver': self.carl.pk,
                                           'message': "Hello"})
        self.assertIn('team', resp.context['form'].errors)
        self.assertEqual(0, Invitation.objects.all().count())

    def test_cannot_invite_if_competition_closed(self):
        """Can't send invites for a closed competition"""
        self.galapagos.is_open = False
        self.galapagos.save()

        with self.loggedInAs("alice", "123"):
            resp = self.client.rpost('invitation_create',
                                     follow=True,
                                     data={'team': self.alice_team.pk,
                                           'receiver': self.carl.pk,
                                           'message': "Hello"})
        self.assertIn('team', resp.context['form'].errors)
        self.assertEqual(0, Invitation.objects.all().count())

    def test_cannot_invite_team_members(self):
        """Can't send invites to already members"""
        self.alice_team.add_team_member(self.carl)
        with self.loggedInAs("alice", "123"):
            resp = self.client.rpost('invitation_create',
                                     follow=True,
                                     data={'team': self.alice_team.pk,
                                           'receiver': self.carl.pk,
                                           'message': "Hello"})
        self.assertIn('receiver', resp.context['form'].errors)
        self.assertEqual(0, Invitation.objects.all().count())

    def test_cannot_send_too_many_invites(self):
        """# of invites <= comp.max_num_team_members"""
        # Add two more users to Alice's team
        self.alice_team.add_team_member(UserFactory.create())
        self.alice_team.add_team_member(UserFactory.create())
        self.assertEqual(0, Invitation.objects.all().count())
        with self.loggedInAs("alice", "123"):
            resp = self.client.rpost('invitation_create',
                                     follow=True,
                                     data={'team': self.alice_team.pk,
                                           'receiver': self.carl.pk,
                                           'message': "Hello"})
        self.assertEqual(0, Invitation.objects.all().count())
        self.assertIn('__all__', resp.context['form'].errors)

    @skip("Not implemented")
    def test_read_invitation_mark_read(self):
        """Reading an invitation marks it as read"""
        pass

    @skip("Not implemented")
    def test_decrease_allowed_invites(self):
        """Team's invite count goes down after sending invite"""
        pass

    @skip("Not implemented")
    def test_invitation_accept(self):
        """Accepting invitations causes user to join team"""
        pass

    @skip("Not implemented")
    def test_registered_to_accept(self):
        """A user cannot accept unless registered to compete"""
        pass

    @skip("Not implemented")
    def test_leave_teams_on_accept(self):
        """Accepting invite causes accepter to leave other teams"""
        # TODO update question to make sure they understand
        pass

    @skip("Not implemented")
    def test_reinviting(self):
        """User can be reinvited after leaving team"""
        pass

    @skip("Not implemented")
    def test_continued_decrease_allowed_invites(self):
        """Team's invite count stays down after accepting invite"""
        pass

    @skip("Not implemented")
    def test_accept_from_another_user(self):
        """Cannot accept an invitation for another person"""
        pass

    @skip("Not implemented")
    def test_invitation_reject(self):
        """Rejecting invitation gets rid of invitation"""
        pass

    @skip("Not implemented")
    def test_can_invite_again(self):
        """User can be invited again after declining"""
        pass

    @skip("Not implemented")
    def test_same_team(self):
        """Rejecting an invitation causes no team change"""
        pass

    @skip("Not implemented")
    def test_increase_allowed_invites(self):
        """After invitee rejects, team gets invite back"""
        pass

    @skip("Not implemented")
    def test_decline_from_another_user(self):
        """Cannot decline invitation for another user"""
        pass

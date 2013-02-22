from django.core.urlresolvers import reverse

from competition.models.invitation_model import Invitation
from competition.tests.utils import FancyTestCase
from competition.tests.factories import (UserFactory, CompetitionFactory,
                                         TeamFactory, InvitationFactory,
                                         RegistrationFactory)

from urllib import urlencode


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

    def test_read_invitation_mark_read(self):
        """Reading an invitation marks it as read"""
        inv = InvitationFactory.create(receiver=self.alice)
        self.assertFalse(inv.read)
        with self.loggedInAs("alice", "123"):
            resp = self.client.rget('invitation_detail', kwargs={'pk': inv.pk})
        # Have to do a whole query, otherwise we won't hit the database
        self.assertTrue(Invitation.objects.get(pk=inv.pk).read)

    def test_decrease_allowed_invites(self):
        """Team's invite count goes down after sending invite"""
        self.assertEqual(2, self.alice_team.num_invites_left())
        InvitationFactory.create(team=self.alice_team)
        self.assertEqual(1, self.alice_team.num_invites_left())
        InvitationFactory.create(team=self.alice_team)
        self.assertEqual(0, self.alice_team.num_invites_left())

    def test_invitation_accept(self):
        """Accepting invitations causes user to join team"""
        # Register Carl to compete
        RegistrationFactory(user=self.carl, competition=self.galapagos)
        # And send him an invitation
        inv = InvitationFactory.create(receiver=self.carl,
                                       team=self.alice_team)
        with self.loggedInAs("carl", "123"):
            resp = self.client.rget('invitation_accept', kwargs={'pk': inv.pk})
            self.assertEqual(200, resp.status_code)
            resp = self.client.rpost('invitation_accept',
                                     follow=True,
                                     kwargs={'pk': inv.pk},
                                     data={'confirmed': True})
            self.assertRedirects(resp, inv.team.get_absolute_url())
        # Set to 'A' for accepted
        self.assertEqual('A', Invitation.objects.get(pk=inv.pk).response)
        self.assertTrue(self.alice_team.is_user_on_team(self.carl))

    def test_registered_to_accept(self):
        """A user cannot accept unless registered to compete"""
        # Carl isn't registered!
        inv = InvitationFactory.create(receiver=self.carl,
                                       team=self.alice_team)
        with self.loggedInAs("carl", "123"):
            # He can still view the invite...
            resp = self.client.rget('invitation_accept', kwargs={'pk': inv.pk})
            self.assertEqual(200, resp.status_code)
            # But he can't accept it without registering
            resp = self.client.rpost('invitation_accept',
                                     follow=True,
                                     kwargs={'pk': inv.pk},
                                     data={'confirmed': True})
        competition_url = inv.team.competition.get_absolute_url()
        invitation_url = inv.get_absolute_url()
        querystring = urlencode({'next': invitation_url})
        redirect_url = competition_url + 'register/?' + querystring
        self.assertRedirects(resp, redirect_url)
        self.assertIsNone(Invitation.objects.get(pk=inv.pk).response)
        self.assertFalse(self.alice_team.is_user_on_team(self.carl))

    def test_leave_teams_on_accept(self):
        """Accepting invite causes accepter to leave other teams"""
        # Register Carl to compete
        RegistrationFactory(user=self.carl, competition=self.galapagos)
        # Put him on a couple of teams
        tg = TeamFactory.create(competition=self.galapagos, num_members=1)
        tg.add_team_member(self.carl)
        ts = TeamFactory.create(competition=self.space, num_members=1)
        ts.add_team_member(self.carl)
        # And send him an invitation to another Galapagos team
        inv = InvitationFactory.create(receiver=self.carl,
                                       team=self.alice_team)
        with self.loggedInAs("carl", "123"):
            resp = self.client.rpost('invitation_accept', follow=True,
                                     kwargs={'pk': inv.pk},
                                     data={'confirmed': True})
        # Carl is only on one Galapagos team
        carl_teams = self.carl.team_set.filter(competition=self.galapagos)
        self.assertEqual(1, carl_teams.count())
        # ... he's on Alice's team
        self.assertTrue(self.alice_team.is_user_on_team(self.carl))
        # ... off the other galapagos team
        self.assertFalse(tg.is_user_on_team(self.carl))
        # ... but still on his space team
        self.assertTrue(ts.is_user_on_team(self.carl))

    def test_reinviting(self):
        """User can be reinvited after leaving team"""
        # Register Carl to compete
        RegistrationFactory(user=self.carl, competition=self.galapagos)
        # And send him an invitation
        inv = InvitationFactory.create(receiver=self.carl,
                                       team=self.alice_team)
        with self.loggedInAs("carl", "123"):
            # Accept invitation
            resp = self.client.rpost('invitation_accept', follow=True,
                                     kwargs={'pk': inv.pk},
                                     data={'confirmed': True})
            self.assertTrue(self.alice_team.is_user_on_team(self.carl))
            self.assertEqual('A', Invitation.objects.get(pk=inv.pk).response)

            # Leave team
            resp = self.client.rpost('team_leave', follow=True,
                                     kwargs={'comp_slug': inv.team.competition.slug},
                                     data={'confirmed': True})
            self.assertFalse(self.alice_team.is_user_on_team(self.carl))

        # Alice forgives him and sends him another invitation
        inv = InvitationFactory.create(receiver=self.carl,
                                       team=self.alice_team)
        with self.loggedInAs("carl", "123"):
            # Accept invitation
            resp = self.client.rpost('invitation_accept', follow=True,
                                     kwargs={'pk': inv.pk},
                                     data={'confirmed': True})
        # Back on Alice's team
        self.assertTrue(self.alice_team.is_user_on_team(self.carl))
        self.assertRedirects(resp, inv.team.get_absolute_url())
        self.assertEqual('A', Invitation.objects.get(pk=inv.pk).response)

    def test_allowed_invites_stays_decreased(self):
        """Team's invite count stays down after accepting invite"""
        # Start with 2 available invites
        self.assertEqual(2, self.alice_team.num_invites_left())

        # Invite carl
        RegistrationFactory(user=self.carl, competition=self.galapagos)
        inv = InvitationFactory.create(receiver=self.carl,
                                       team=self.alice_team)
        # Down to one available invite
        self.assertEqual(1, self.alice_team.num_invites_left())
        with self.loggedInAs("carl", "123"):
            # Accept invitation
            resp = self.client.rpost('invitation_accept', follow=True,
                                     kwargs={'pk': inv.pk},
                                     data={'confirmed': True})
        # Still only have one available invite
        self.assertTrue(self.alice_team.is_user_on_team(self.carl))
        self.assertEqual(1, self.alice_team.num_invites_left())

    def test_accept_from_another_user(self):
        """Cannot accept an invitation for another person"""
        # Invite carl
        RegistrationFactory(user=self.carl, competition=self.galapagos)
        inv = InvitationFactory.create(receiver=self.carl,
                                       team=self.alice_team)
        with self.loggedInAs("alice", "123"):
            # Try to accept as alice
            resp = self.client.rpost('invitation_accept', follow=True,
                                     kwargs={'pk': inv.pk},
                                     data={'confirmed': True})
            self.assert404(resp)
        with self.loggedInAs("bob", "123"):
            # Try to accept as bob
            resp = self.client.rpost('invitation_accept', follow=True,
                                     kwargs={'pk': inv.pk},
                                     data={'confirmed': True})
            self.assert404(resp)
        self.assertFalse(self.alice_team.is_user_on_team(self.carl))

    def test_invitation_reject(self):
        """Rejecting invitation gets rid of invitation"""
        # Register Carl to compete
        RegistrationFactory(user=self.carl, competition=self.galapagos)
        # And send him an invitation
        inv = InvitationFactory.create(receiver=self.carl,
                                       team=self.alice_team)
        with self.loggedInAs("carl", "123"):
            resp = self.client.rget('invitation_decline', kwargs={'pk': inv.pk})
            self.assertEqual(200, resp.status_code)
            # Decline invitation
            resp = self.client.rpost('invitation_decline', follow=True,
                                     kwargs={'pk': inv.pk},
                                     data={'confirmed': True})
            self.assertRedirects(resp, inv.team.competition.get_absolute_url())
        # Set to 'D' for declined
        self.assertEqual('D', Invitation.objects.get(pk=inv.pk).response)
        self.assertFalse(self.alice_team.is_user_on_team(self.carl))

    def test_can_invite_again(self):
        """User can be invited again after declining"""
        # Register Carl to compete
        RegistrationFactory(user=self.carl, competition=self.galapagos)
        # And send him an invitation
        inv = InvitationFactory.create(receiver=self.carl,
                                       team=self.alice_team)
        with self.loggedInAs("carl", "123"):
            # Decline invitation
            resp = self.client.rpost('invitation_decline', follow=True,
                                     kwargs={'pk': inv.pk},
                                     data={'confirmed': True})
            self.assertFalse(self.alice_team.is_user_on_team(self.carl))

        # Alice is persistent. Sends another invitation
        inv = InvitationFactory.create(receiver=self.carl,
                                       team=self.alice_team)
        with self.loggedInAs("carl", "123"):
            # Carl accepts this time
            resp = self.client.rpost('invitation_accept', follow=True,
                                     kwargs={'pk': inv.pk},
                                     data={'confirmed': True})
        self.assertTrue(self.alice_team.is_user_on_team(self.carl))

    def test_same_team(self):
        """Rejecting an invitation causes no team change"""
        # Register Carl to compete
        RegistrationFactory(user=self.carl, competition=self.galapagos)
        # Put him on a team
        carl_team = TeamFactory.create(competition=self.galapagos,
                                       num_members=1)
        carl_team.add_team_member(self.carl)

        # Alice sends him an invitation
        inv = InvitationFactory.create(receiver=self.carl,
                                       team=self.alice_team)
        with self.loggedInAs("carl", "123"):
            # Carl declines invitation
            resp = self.client.rpost('invitation_decline', follow=True,
                                     kwargs={'pk': inv.pk},
                                     data={'confirmed': True})
        # Carl isn't on Alice's team, and he's still on his old team
        self.assertFalse(self.alice_team.is_user_on_team(self.carl))
        self.assertTrue(carl_team.is_user_on_team(self.carl))

    def test_increase_allowed_invites(self):
        """After invitee rejects, team gets invite back"""
        # Register Carl to compete
        RegistrationFactory(user=self.carl, competition=self.galapagos)
        # Alice's team has two available invites
        self.assertEqual(2, self.alice_team.num_invites_left())
        # Alice sends him an invitation
        inv = InvitationFactory.create(receiver=self.carl,
                                       team=self.alice_team)
        # Alice's team now has one available invite
        self.assertEqual(1, self.alice_team.num_invites_left())
        with self.loggedInAs("carl", "123"):
            # Carl declines invitation
            resp = self.client.rpost('invitation_decline', follow=True,
                                     kwargs={'pk': inv.pk},
                                     data={'confirmed': True})
        # Alice's team has two invites again
        self.assertEqual(2, self.alice_team.num_invites_left())

    def test_decline_from_another_user(self):
        """Cannot decline invitation for another user"""
        # Invite carl
        RegistrationFactory(user=self.carl, competition=self.galapagos)
        inv = InvitationFactory.create(receiver=self.carl,
                                       team=self.alice_team)
        with self.loggedInAs("alice", "123"):
            # Try to decline as alice
            resp = self.client.rpost('invitation_decline', follow=True,
                                     kwargs={'pk': inv.pk},
                                     data={'confirmed': True})
            self.assert404(resp)
        with self.loggedInAs("bob", "123"):
            # Try to decline as bob
            resp = self.client.rpost('invitation_decline', follow=True,
                                     kwargs={'pk': inv.pk},
                                     data={'confirmed': True})
            self.assert404(resp)
        self.assertIsNone(Invitation.objects.get(pk=inv.pk).response)

    def test_cannot_decline_twice(self):
        """Cannot decline an invitation more than once"""
        # Invite carl
        RegistrationFactory(user=self.carl, competition=self.galapagos)
        inv = InvitationFactory.create(receiver=self.carl,
                                       team=self.alice_team)
        with self.loggedInAs("carl", "123"):
            # Decline
            self.client.rpost('invitation_decline', follow=True,
                              kwargs={'pk': inv.pk}, data={'confirmed': True})
            self.assertEqual('D', Invitation.objects.get(pk=inv.pk).response)

            # Decline again
            resp = self.client.rpost('invitation_decline', follow=True,
                                     kwargs={'pk': inv.pk},
                                     data={'confirmed': True})
            # Didn't work the second time
            self.assert404(resp)
            # Still declined, though
            self.assertEqual('D', Invitation.objects.get(pk=inv.pk).response)

    def test_cannot_accept_twice(self):
        """Cannot accept an invitation more than once"""
        # Invite carl
        RegistrationFactory(user=self.carl, competition=self.galapagos)
        inv = InvitationFactory.create(receiver=self.carl,
                                       team=self.alice_team)
        with self.loggedInAs("carl", "123"):
            # Accept
            self.client.rpost('invitation_accept', follow=True,
                              kwargs={'pk': inv.pk}, data={'confirmed': True})
            self.assertEqual('A', Invitation.objects.get(pk=inv.pk).response)

            # Accept again
            resp = self.client.rpost('invitation_accept', follow=True,
                                     kwargs={'pk': inv.pk},
                                     data={'confirmed': True})
            # Didn't work the second time
            self.assert404(resp)
            # Still accepted, though
            self.assertEqual('A', Invitation.objects.get(pk=inv.pk).response)

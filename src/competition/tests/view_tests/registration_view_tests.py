from django.core.urlresolvers import reverse

from competition.models.registration_model import Registration
from competition.tests.utils import FancyTestCase

from competition.tests.factories import (UserFactory, CompetitionFactory,
                                         RegistrationFactory)
from competition.tests.factories import RegistrationQuestionFactory as QuestionFactory

from unittest import skip
import random


class RegistrationViewsTest(FancyTestCase):

    def setUp(self):
        self.alice = UserFactory.create(username="alice")
        self.space = CompetitionFactory.create(name="Space")
        self.galapagos = CompetitionFactory.create(name="Galapagos")
        self.galapagos.is_open = True
        self.galapagos.save()

        self.questions = [QuestionFactory.create(question_type=t)
                          for t in ('SA', 'MC', 'AB', 'SC')]
        self.galapagos.questions.add(*self.questions)

    def fill_in_forms(self, response):
        """Fills in a registration form with random data 

        Assumes that ``response``'s context contains a ``questions``
        item, which we can iterate through and fill in

        Returns a dict suitable to POST as data
        """
        forms = [x[1] for x in response.context['questions']]

        # Create a dict of all fields {'prefix-field_name': field, ...}
        fields = dict(("%d-%s" % (f.prefix, field_name), field)
                      for f in forms
                      for field_name, field in f.fields.iteritems())

        data = {}
        for name, field in fields.iteritems():
            if 'sa_response' in name:
                data[name] = "derp"
            elif 'ab_response' in name:
                data[name] = True
            else:
                choices = [x[0] for x in field.choices]
                random.shuffle(choices)
                if 'sc_response' in name:
                    data[name] = choices[0]
                elif 'mc_response' in name:
                    # Choose more than one option
                    num_choices = (len(choices) / 2) + 1
                    data[name] = choices[:num_choices]
        return data

    def test_authentication(self):
        """Users must be logged in to register"""
        kwds = {'comp_slug': self.galapagos.slug}
        register_url = reverse("register_for", kwargs=kwds)
        response = self.client.get(register_url)
        self.assertRedirects(response,
                             '/accounts/login/?next=' + register_url)

        with self.loggedInAs("alice", "123"):
            response = self.client.get(register_url)
            self.assertEqual(200, response.status_code)

    def test_get_register_page(self):
        """Users should see some details about the competition and a
        list of forms with the competition's registration questions."""
        with self.loggedInAs("alice", "123"):
            kwds = {'comp_slug': self.galapagos.slug}
            response = self.client.rget("register_for", kwargs=kwds)
            self.assertIn("competition", response.context)
            self.assertIn("questions", response.context)

            forms = response.context['questions']
            self.assertEqual(len(self.questions), len(forms))

    def test_post_register_page(self):
        """A registration object should be created when users submit
        their form"""
        num_registrations = Registration.objects.count()
        kwds = {'comp_slug': self.galapagos.slug}
        with self.loggedInAs("alice", "123"):
            response = self.client.rget("register_for", kwargs=kwds)

            response = self.client.rpost("register_for", kwargs=kwds,
                                         data=self.fill_in_forms(response))
            # Should have one more registration now.
            self.assertEqual(num_registrations + 1,
                             Registration.objects.count())

    def test_logout_mid_register(self):
        """Users should be redirected if they logout early."""
        kwds = {'comp_slug': self.galapagos.slug}
        register_url = reverse("register_for", kwargs=kwds)
        with self.loggedInAs("alice", "123"):
            self.client.get(register_url)

        with self.loggedInAs("alice", "123"):
            response = self.client.post(register_url, follow=True)

        messages = list(response.context['messages'])
        self.assertEqual(1, len(messages))
        self.assertIn("session", messages[0].message)
        self.assertRedirects(response, register_url)

    def test_altered_questions(self):
        """Users should have to re-enter forms if questions are
        changed while the form's being filled out"""
        kwds = {'comp_slug': self.galapagos.slug}
        register_url = reverse("register_for", kwargs=kwds)
        with self.loggedInAs("alice", "123"):
            response = self.client.get(register_url)

            # Fill in old form
            data = self.fill_in_forms(response)

            # Add a new question
            self.galapagos.questions.add(QuestionFactory.create())

            # Submit old form... which should redirect
            response = self.client.post(register_url, data=data, follow=True)

        messages = list(response.context['messages'])
        self.assertEqual(1, len(messages))
        self.assertIn("changed", messages[0].message)
        self.assertRedirects(response, register_url)

    def test_registered_users_cannot_view_register_page(self):
        """Users shouldn't be able to view the registration page once
        they have an active registration"""
        # Register Alice
        RegistrationFactory.create(user=self.alice, competition=self.galapagos)
        with self.loggedInAs("alice", "123"):
            kwargs = {'comp_slug': self.galapagos.slug}
            response = self.client.rget("register_for", follow=True,
                                        kwargs=kwargs)

        self.assertEqual(1, Registration.objects.all().count()) # still only 1
        messages = list(response.context['messages'])
        self.assertEqual(1, len(messages))
        self.assertIn("already", messages[0].message)
        self.assertRedirects(response, self.galapagos.get_absolute_url())

    def test_registered_users_cannot_resubmit(self):
        """Users shouldn't be able to submit a new registration once
        they have an active registration, """
        kwds = {'comp_slug': self.galapagos.slug}
        register_url = reverse("register_for", kwargs=kwds)
        with self.loggedInAs("alice", "123"):
            response = self.client.get(register_url)
            data = self.fill_in_forms(response)
            self.client.post(register_url, follow=True, data=data)
            self.assertEqual(1, Registration.objects.all().count()) # Only 1

        # Nothing should happen if we resubmit the form
        with self.loggedInAs("alice", "123"):
            response = self.client.post(register_url, follow=True, data=data)

        self.assertEqual(1, Registration.objects.all().count()) # Still only 1

        messages = list(response.context['messages'])
        self.assertEqual(1, len(messages))
        self.assertIn("already", messages[0].message)
        self.assertRedirects(response, self.galapagos.get_absolute_url())

    def test_active_users_can_deactivate(self):
        """If a user has an active registration, they should be able
        to deactivate."""
        RegistrationFactory.create(user=self.alice, competition=self.galapagos)

        # Try viewing the unregister page
        with self.loggedInAs("alice", "123"):
            resp = self.client.rget('unregister_for',
                                    kwargs={'comp_slug': self.galapagos.slug})

        # Make sure we got the confirmation form
        self.assertIn('question', resp.context)
        self.assertIn('form', resp.context)

        with self.loggedInAs("alice", "123"):
            resp = self.client.rpost('unregister_for', follow=True,
                                     kwargs={'comp_slug': self.galapagos.slug},
                                     data={'confirmed': True})

        # No active registrations, but one inactive one.
        self.assertEqual(0, Registration.objects.filter(active=True).count())
        self.assertEqual(1, Registration.objects.filter(active=False).count())

        messages = list(resp.context['messages'])
        self.assertEqual(1, len(messages))
        self.assertIn("unregistered", messages[0].message)
        self.assertRedirects(resp, self.galapagos.get_absolute_url())

    def test_inactive_users_can_register(self):
        """If a user has an inactive registration, they should be able
        to register again."""
        registration = RegistrationFactory.create(user=self.alice,
                                                  competition=self.galapagos)
        registration.deactivate()

        kwds = {'comp_slug': self.galapagos.slug}
        register_url = reverse("register_for", kwargs=kwds)
        with self.loggedInAs("alice", "123"):
            resp = self.client.get(register_url)
            data = self.fill_in_forms(resp)
            resp = self.client.post(register_url, follow=True, data=data)

        # Two registrations, one active, one inactive.
        self.assertEqual(1, Registration.objects.filter(active=True).count())
        self.assertEqual(1, Registration.objects.filter(active=False).count())

    def test_unregistered_users_cannot_deactivate(self):
        """Users cannot deactivate a registration if they aren't
        registered"""
        # Try viewing the unregister page
        with self.loggedInAs("alice", "123"):
            resp = self.client.rget('unregister_for',
                                    kwargs={'comp_slug': self.galapagos.slug})

        # We should get a 404 since the user isn't registered
        self.assertEqual(404, resp.status_code)

        with self.loggedInAs("alice", "123"):
            resp = self.client.rpost('unregister_for', follow=True,
                                     kwargs={'comp_slug': self.galapagos.slug},
                                     data={'confirmed': True})

        # We should get a 404 for a POST as well.
        self.assertEqual(404, resp.status_code)

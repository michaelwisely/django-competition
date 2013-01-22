from django.core.urlresolvers import reverse

from competition.models.registration_model import Registration
from competition.tests.utils import FancyTestCase

from competition.tests.factories import UserFactory, CompetitionFactory
from competition.tests.factories import RegistrationQuestionFactory as QuestionFactory

import unittest
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
            kwds = {'comp_slug': self.galapagos.slug}
            response = self.client.rget("register_for", kwargs=kwds)
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

    @unittest.skip
    def test_users_cannot_reregister(self):
        """Once a user registers, they shouldn't be able to register
        again."""
        pass

    

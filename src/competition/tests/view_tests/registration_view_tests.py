from django.http import Http404
from django.contrib.auth.models import User

from competition.models.registration_model import Registration
from competition.models.competition_model import Competition
from competition.tests.utils import FancyTestCase

from unittest import skip


class RegistrationViewsTest(FancyTestCase):
    fixtures = ['competition_test_data.yaml',
                'user_test_data.yaml',
                'registration_test_data.yaml',
                'registration_question_test_data.yaml']

    def setUp(self):
        self.alice = User.objects.get(username="alice")
        self.space = Competition.objects.get(slug__contains="space")
        self.galapagos = Competition.objects.get(slug__contains="galapagos")
        self.galapagos.is_open = True
        self.galapagos.save()

    @skip("Not implemented")
    def test_authentication(self):
        """Users must be logged in to register"""
        with self.assertRaises(Http404):
            kwds = {'comp_slug': self.galapagos.slug}
            self.client.rget("register_for", kwargs=kwds)
        with self.loggedInAs("alice", "123"):
            kwds = {'comp_slug': self.galapagos.slug}
            self.client.rget("register_for", kwargs=kwds)

    @skip("Not implemented")
    def test_get_register_page(self):
        """Users should see some details about the competition and a
        formset with the competitoin's registration questions."""
        with self.loggedInAs("alice", "123"):
            kwds = {'comp_slug': self.galapagos.slug}
            response = self.client.rget("register_for", kwargs=kwds)
            self.assertIn("competition", response.context)
            self.assertIn("formset", response.context)  # questions

            formset = response.context['formset']
            self.assertEqual(4, formset.total_form_count())

    @skip("Not implemented")
    def test_post_register_page(self):
        """A registration object should be created when users submit
        their form"""
        num_registrations = Registration.objects.count()
        with self.loggedInAs("alice", "123"):
            # Not sure if we need to do a get before this post
            data = {'form-0-text_response': "No allergies",
                    'form-1-agreed': True,
                    'form-2-choices': 6,  # Large shirt
                    'form-3-choices': [1, 2]}   # cheese and pepperoni
            kwds = {'comp_slug': self.galapagos.slug}
            response = self.client.rpost("register_for", 
                                         kwargs=kwds, data=data)
            # Should have one more registration now.
            self.assertEqual(num_registrations + 1, 
                             Registration.objects.count())

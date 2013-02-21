from django.test import TestCase
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from competition.tests.factories import (CompetitionFactory,
                                         RegistrationFactory,
                                         UserFactory)
from competition.models import Competition

from datetime import datetime, timedelta


TWELVE_HOURS = timedelta(hours=12)


class CompetitionModelValidationTest(TestCase):

    def test_reasonable_name(self):
        """Valid competition names should pass"""
        c = CompetitionFactory.build(name="MegaMinerAI 10: -B.O.N.K-")
        c.full_clean()

    def test_name_validation(self):
        """Competition names must pass the name validator"""
        c = CompetitionFactory.build(name="{no way}")

        with self.assertRaises(ValidationError) as cm:
            c.full_clean()

        self.assertEqual(1, len(cm.exception.message_dict))
        self.assertIn("name", cm.exception.message_dict)

    def test_name_is_sluggable(self):
        """Competition names must be sluggable"""
        now = datetime.now()
        c = CompetitionFactory.build(name="..")

        with self.assertRaises(ValidationError) as cm:
            c.full_clean()

        self.assertEqual(1, len(cm.exception.message_dict))
        self.assertIn("name", cm.exception.message_dict)

    def test_valid_start_end_times(self):
        """Start time must be before end time"""
        twelve_hours_ago = datetime.now() - TWELVE_HOURS
        c = CompetitionFactory.build(end_time=twelve_hours_ago)

        with self.assertRaises(ValidationError) as cm:
            c.full_clean()

        self.assertEqual(1, len(cm.exception.message_dict))
        self.assertIn("__all__", cm.exception.message_dict)


    def test_valid_team_sizes(self):
        """Max team size must be greater than min team size"""
        c = CompetitionFactory.build(min_num_team_members=2,
                                     max_num_team_members=1)

        with self.assertRaises(ValidationError) as cm:
            c.full_clean()

        self.assertEqual(1, len(cm.exception.message_dict))
        self.assertIn("__all__", cm.exception.message_dict)

    def test_positive_min_team_size(self):
        """Team min sizes must be greater than 0"""
        c = CompetitionFactory.build(min_num_team_members=-1)

        with self.assertRaises(ValidationError) as cm:
            c.full_clean()

        self.assertEqual(1, len(cm.exception.message_dict))
        self.assertIn("min_num_team_members", cm.exception.message_dict)

    def test_positive_max_team_size(self):
        """Team max sizes must be greater than 0"""
        c = CompetitionFactory.build(max_num_team_members=-1)

        with self.assertRaises(ValidationError) as cm:
            c.full_clean()

        self.assertEqual(2, len(cm.exception.message_dict))
        self.assertIn("max_num_team_members", cm.exception.message_dict)

    def test_positive_cost(self):
        """Cost must be greater than 0"""
        c = CompetitionFactory.build(cost_per_person=-20.3)

        with self.assertRaises(ValidationError) as cm:
            c.full_clean()

        self.assertEqual(1, len(cm.exception.message_dict))
        self.assertIn("cost_per_person", cm.exception.message_dict)

    def test_slug_set(self):
        """Competition slug should be set when it's saved"""
        c = CompetitionFactory.build()
        self.assertEqual('', c.slug)
        c.save()
        self.assertEqual(slugify(c.name), c.slug)

    def test_no_duplicate_names(self):
        """Make sure we can't have two competitions by the same name"""
        CompetitionFactory.create(name="MegaMinerAI")
        with self.assertRaises(IntegrityError):
            CompetitionFactory.create(name="MegaMinerAI")

    def test_registrated_for_user(self):
        """List competition where a user is registered"""
        c1 = CompetitionFactory.create(name="MegaMinerAI1")
        c2 = CompetitionFactory.create(name="MegaMinerAI2")
        c3 = CompetitionFactory.create(name="MegaMinerAI3")
        alice = UserFactory.create()
        RegistrationFactory.create(user=alice, competition=c1)
        RegistrationFactory.create(user=alice, competition=c3)
        l = list(Competition.objects.user_registered(alice))
        self.assertEqual(2, len(l))
        self.assertIn(c1, l)
        self.assertIn(c3, l)

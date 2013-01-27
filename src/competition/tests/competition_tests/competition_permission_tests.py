from django.test import TestCase
from django.contrib.auth.models import Group
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from competition.tests.factories import CompetitionFactory
from competition.models import Competition


class CompetitionPermissionTest(TestCase):

    def setUp(self):
        self.permissions = ['add_competition',
                            'change_competition',
                            'delete_competition']

    def test_group_created(self):
        """Group is created on syncdb"""
        group_query = Group.objects.filter(name="Competition Staff")
        self.assertFalse(group_query.exists())

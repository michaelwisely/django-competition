from django.test import TestCase

from competition.models.competition_model import Competition
from competition.tests.factories import (CompetitionFactory, UserFactory,
                                         OrganizerFactory)


class OrganizerModelTest(TestCase):

    def setUp(self):
        self.alice = UserFactory.create(username="alice")

        self.space = CompetitionFactory.create(name="Space")
        self.galapagos = CompetitionFactory.create(name="Galapagos")

        self.space_org = OrganizerFactory.create(user=self.alice,
                                                 competition=self.space)
        self.galapagos_org = OrganizerFactory.create(user=self.alice,
                                                     competition=self.galapagos)

    def test_permissions_set(self):
        """Organizers permissions are set when created"""
        for permission in Competition.get_organizer_permissions():
            # Have both space and galapagos perms
            self.assertTrue(self.alice.has_perm(permission, self.space))
            self.assertTrue(self.alice.has_perm(permission, self.galapagos))

    def test_permissions_removed(self):
        """Organizers permissions are removed when deleted"""
        self.space_org.delete()
        for permission in Competition.get_organizer_permissions():
            # No longer have space perms
            self.assertFalse(self.alice.has_perm(permission, self.space))
            # But still have galapagos perms
            self.assertTrue(self.alice.has_perm(permission, self.galapagos))

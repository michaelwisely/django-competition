from django.test import TestCase
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError

from competition.validators import greater_than_zero, non_negative, validate_name


class ValidationFunctionTest(TestCase):

    def test_greater_than_zero(self):
        """Check greater_than_zero validator"""
        self.assertRaises(ValidationError, greater_than_zero, 0)
        self.assertRaises(ValidationError, greater_than_zero, -1)
        self.assertIsNone(greater_than_zero(1))

    def test_non_negative(self):
        """Check non_negative validator"""
        self.assertRaises(ValidationError, non_negative, -1)
        self.assertIsNone(non_negative(0))
        self.assertIsNone(non_negative(1))

    def test_validate_name(self):
        """Check name validator"""
        # Try some valid names
        valid_names = ['MegaMiner-AI 10: Galapagos', 'Chess 2012', '2012 Chess',
                       'B.L.O.O.M. 2: Revenge of the Flowers']
        for name in valid_names:
            self.assertIsNone(validate_name(name))

        self.assertRaises(ValidationError, validate_name, "..")
        self.assertRaises(ValidationError, validate_name, "_..")
        self.assertRaises(ValidationError, validate_name, "_")
        self.assertRaises(ValidationError, validate_name, "____")
        self.assertRaises(ValidationError, validate_name, ".Nope")
        self.assertRaises(ValidationError, validate_name, ".Nope")

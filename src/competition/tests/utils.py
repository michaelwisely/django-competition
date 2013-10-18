from django.test.client import Client
from django.test import TestCase as DjangoTestCase
from django.core.urlresolvers import reverse

import contextlib


class FancyClient(Client):

    def _get_url(self, viewname, args, kwargs):
        args = () if args is None else args
        kwargs = {} if kwargs is None else kwargs
        return reverse(viewname, args=args, kwargs=kwargs)

    def rget(self, viewname, args=None, kwargs=None, data=None, **extras):
        """Does a reverse before doing a get"""
        data = {} if data is None else data
        url = self._get_url(viewname, args, kwargs)
        return self.get(url, data=data, **extras)

    def rpost(self, viewname, args=None, kwargs=None, data=None, **extras):
        """Does a reverse before doing a post"""
        data = {} if data is None else data
        url = self._get_url(viewname, args, kwargs)
        return self.post(url, data=data, **extras)


class FancyTestCase(DjangoTestCase):
    client_class = FancyClient

    # @property
    # def client(self):
    #     if not hasattr(self, "_client"):
    #         self._client = self.client_class()
    #     return self._client

    @contextlib.contextmanager
    def loggedInAs(self, username, password):
        """Provides a context in which a given user is logged in.

        Example usage::

        with login_as("alice", "secret") as client:
            client.get("/")
        """
        self.client.login(username=username, password=password)
        yield
        self.client.logout()

    def assert404(self, response):
        return self.assertEqual(404, response.status_code)

    def assertInGroup(self, user, group):
        return self.assertTrue(user.groups.filter(name=group.name).exists())

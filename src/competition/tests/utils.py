from django.test.client import Client
from django.test import TestCase as DjangoTestCase
from django.core.urlresolvers import reverse

import contextlib


class FancyClient(Client):
    def rget(self, viewname, args=None, kwargs=None):
        """Does a reverse before doing a get"""
        args = [] if args is None else args
        kwargs = {} if kwargs is None else kwargs
        return self.get(reverse(viewname), args, kwargs)

    def rpost(self, viewname, args=None, kwargs=None):
        """Does a reverse before doing a post"""
        args = [] if args is None else args
        kwargs = {} if kwargs is None else kwargs
        return self.post(reverse(viewname), args, kwargs)


@contextlib.contextmanager
def login_as(username, password):
    """Provides a context in which a given user is logged in.
    
    Example usage::

        with login_as("alice", "secret") as client:
            client.get("/")

    """
    c = FancyClient()
    c.login(username=username, password=password)
    yield c
    c.logout()


class FancyTestCase(DjangoTestCase):
    client_class = FancyClient
    
    def loggedInAs(self, username, password):
        """Creates and returns a context as a logged in user"""
        return login_as(username, password)
 

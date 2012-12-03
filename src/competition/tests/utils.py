class FancyClient(Client):
    def rget(viewname, args, kwargs):
        """Does a reverse before doing a get"""
        pass

    def rpost(viewname, args, kwargs):
        """Does a reverse before doing a post"""
        pass

class FancyTestCase(TestCase):
    def loggedInAs(username, password):
        """Creates and returns a context as a logged in user"""
        # TODO implement
        pass

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404

from piston.handler import BaseHandler
from piston.authentication import HttpBasicAuthentication

from competition.models.competition_model import Competition
from competition.utility import competitor_search_filter


class HttpSessionAuthentication(HttpBasicAuthentication):

    def is_authenticated(self, request):
        # If the user is authenticated with a session, let them through.
        try:
            session = Session.objects.get(pk=request.COOKIES['sessionid'])
            user = User.objects.get(pk=session.get_decoded()['_auth_user_id'])
            if user.is_authenticated():
                return True
        except (KeyError, Session.DoesNotExist):
            pass

        # Otherwise, see if they've provided HTTPBasicAuth
        return super(HttpSessionAuthentication, self).is_authenticated(request)

    def __repr__(self):
        return u'<HTTPSession: realm=%s>' % self.realm


class CompetitiorHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = User
    fields = ('username', 'first_name', 'last_name', 'get_full_name')

    def read(self, request, search=None, comp_slug=None, free=False):
        users = User.objects
        if comp_slug != None:
            c = get_object_or_404(Competition, slug=comp_slug)
            users = users.filter(registration__competition=c)
            if free:
                users = users.exclude(team__competition=c)
        users = users.filter(registration__active=True)
        if search != None:
            users = competitor_search_filter(users, search)
        return users

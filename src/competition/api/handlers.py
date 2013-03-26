from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from piston.handler import BaseHandler

from competition.models.team_model import Team
from competition.models.competition_model import Competition
from competition.utility import competitor_search_filter 

import re

class CompetitiorHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = User
    fields = ('username','first_name','last_name','get_full_name')
    
    def read(self, request, search=None, comp_slug=None, free=False):
        users = User.objects
        if comp_slug != None:
            c = get_object_or_404(Competition,slug=comp_slug)
            users = users.filter(registration__competition=c)
            if free:
                users = users.exclude(team__competition=c)
        users = users.filter(registration__active=True)
        if search != None:
            users = competitor_search_filter(users,search)
        return users

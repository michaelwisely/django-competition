from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from competition.models import Team, Competition

from .serializers import TeamSerializer, UserSerializer


class TeamListAPIView(generics.ListAPIView):
    """Lists Teams for a particular competition

    Returns an **HTTP 200** if successful, with a JSON object full of
    information.

    """
    serializer_class = TeamSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        comp_slug = self.kwargs['comp_slug']
        return Team.objects.filter(competition__slug=comp_slug)


class FreeAgentListAPIView(generics.ListAPIView):
    """Lists FreeAgents for a particular competition

    Returns an **HTTP 200** if successful, with a JSON object full of
    information.

    """
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        comp = get_object_or_404(Competition, slug=self.kwargs['comp_slug'])
        users = User.objects.filter(registration__competition=comp,
                                    registration__active=True)
        return users.exclude(team__competition=comp)

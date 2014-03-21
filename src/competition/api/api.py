from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from competition.models import Game

from .serializers import GameSerializer


class GameListAPIView(generics.ListAPIView):
    """Lists games played by a particular team

    Returns an **HTTP 200** if successful, with a JSON object full of
    information.

    """
    serializer_class = GameSerializer
    permission_classes = (IsAuthenticated,)
    paginate_by = 100

    def get_queryset(self):
        user = self.request.user
        comp_slug = self.kwargs['comp_slug']
        team = get_object_or_404(user.team_set, competition__slug=comp_slug)
        return team.game_set.all()

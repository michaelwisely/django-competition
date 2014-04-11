from django.contrib.auth.models import User
from rest_framework import serializers
from competition.models import Game, GameScore, Team


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ('name', 'slug', 'url')

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, obj):
        return obj.get_absolute_url()


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('id', 'game_id', 'created', 'teams', 'data')

    teams = serializers.SerializerMethodField('get_teams')
    data = serializers.SerializerMethodField('get_data')

    def get_teams(self, obj):
        return TeamSerializer(obj.teams.all(), many=True).data

    def get_data(self, obj):
        return obj.data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'url')

    name = serializers.SerializerMethodField('get_name')
    url = serializers.SerializerMethodField('get_url')

    def get_name(self, obj):
        username = obj.username
        full_name = obj.get_full_name()
        if full_name:
            return "{} ({})".format(username, full_name)
        return username

    def get_url(self, obj):
        return obj.get_absolute_url()

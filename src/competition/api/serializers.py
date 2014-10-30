from django.contrib.auth.models import User

from rest_framework import serializers

from competition.models import Team


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ('name', 'slug', 'url')

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, obj):
        return obj.get_absolute_url()


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
            return u"{} ({})".format(username, full_name)
        return username

    def get_url(self, obj):
        return obj.get_absolute_url()

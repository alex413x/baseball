from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from baseball.models import Match, Player, Stat, Pitch


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups',)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name',)


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Match
        fields = ('id', 'created',)


class StatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stat
        fields = ('id', 'created', 'category', 'name', 'abbr', 'value_str', 'value', 'date', 'league')


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    # stats = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    #stats = StatSerializer(many=True, read_only=True)
    class Meta:
        model = Player
        # fields = Player._meta.get_all_field_names() + ['stats']
        fields = ('id', 'created', 'first_name', 'last_name')

class PlayerDetailSerializer(serializers.HyperlinkedModelSerializer):
    stats = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Player
        fields = Player._meta.get_all_field_names() + ['stats']


class PitchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pitch
        # fields = ('id', 'created', 'batter', 'pitcher')
        fields = Pitch._meta.get_all_field_names()


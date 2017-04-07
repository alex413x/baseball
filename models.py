from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.db import models
from django.contrib.postgres.fields import JSONField
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

from faker import Faker
fake = Faker()

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

def emptyJSON():
    return {}


class Average(models.Model):

    class Meta:
        ordering = ('created',)

    def __str__(self):              # __unicode__ on Python 2
        return "Average for %s of league %s" % (self.name, self.league)

    created = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(blank=True, null=True)
    league = models.CharField(max_length=30, default='')
    name = models.CharField(max_length=30, default='')
    value = models.DecimalField(max_digits=19, decimal_places=7, default=0)


class Match(models.Model):

    class Meta:
        ordering = ('created',)

    def __str__(self):              # __unicode__ on Python 2
        return "%s %s" % (self.first_name, self.last_name)

    created = models.DateTimeField(auto_now_add=True)


class Player(models.Model):

    class Meta:
        ordering = ('created',)

    def __str__(self):              # __unicode__ on Python 2
        return "%s %s" % (self.first_name, self.last_name)

    created = models.DateTimeField(auto_now_add=True)
    player_id = models.CharField(max_length=30, default=fake.first_name())

    first_name = models.CharField(max_length=30, default=fake.first_name())
    middle_name = models.CharField(max_length=30, default=fake.first_name())
    last_name = models.CharField(max_length=30, default=fake.last_name())
    nick_name = models.CharField(max_length=30, default='')
    birth_date = models.DateTimeField(blank=True, null=True)
    birth_country = models.CharField(max_length=30, default=fake.country())
    birth_state = models.CharField(max_length=30, default=fake.state())
    birth_city = models.CharField(max_length=30, default=fake.city())
    death_date = models.DateTimeField(blank=True, null=True)
    death_country = models.CharField(max_length=30, default=fake.country())
    death_state = models.CharField(max_length=30, default=fake.state())
    death_city = models.CharField(max_length=30, default=fake.city())
    debut = models.DateTimeField(blank=True, null=True)
    final_game = models.DateTimeField(blank=True, null=True)
    retro_id = models.CharField(max_length=30, default=fake.first_name())
    bbref_id = models.CharField(max_length=30, default=fake.first_name())
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    handidness = (
        ('L', 'Left'),
        ('R', 'Right'),
        ('B', 'Both'),
    )
    bats = models.CharField(max_length=30, default='', choices=handidness)
    throws = models.CharField(max_length=30, default='', choices=handidness)

class Stat(models.Model):

    player = models.ForeignKey(Player, related_name="stats", null=True, blank=True)
    cat_choices = [i for i in enumerate([
     'Teams',
     'AwardsManagers',
     'SeriesPost',
     'TeamsHalf',
     'Salaries',
     'Managers',
     'HomeGames',
     'AllstarFull',
     'AwardsSharePlayers',
     'FieldingOF',
     'Fielding',
     'CollegePlaying',
     'ManagersHalf',
     'PitchingPost',
     'Appearances',
     'Schools',
     'Pitching',
     'HallOfFame',
     'Batting',
     'AwardsPlayers',
     'BattingPost',
     'FieldingPost',
     'Master',
     'AwardsShareManagers',
     'Parks',
     'TeamsFranchises']
    )]
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(blank=True, null=True)
    league = models.CharField(max_length=30, default='')
    category = models.CharField(max_length=30, default='', choices=cat_choices)
    name = models.CharField(max_length=30, default='')
    abbr = models.CharField(max_length=30, default='')
    value_str = models.CharField(max_length=30, default='')
    value = models.DecimalField(max_digits=19, decimal_places=7, default=0)

    class Meta:
        ordering = ['name', 'player']

    def __str__(self):              # __unicode__ on Python 2
        return "%s" % self.name


class Pitch(models.Model):

    class Meta:
        ordering = ('created',)

    def __str__(self):              # __unicode__ on Python 2
        return "%s" % self.id

    created = models.DateTimeField(auto_now_add=True)
    batter = models.ForeignKey(Player, related_name="batter", null=True, blank=True)
    pitcher = models.ForeignKey(Player, related_name="pitcher", null=True, blank=True)
    status = models.CharField(max_length=30, default='initialized')
    result = models.TextField(max_length=700, default='None')
    default_method = models.CharField(max_length=30, default='odds_ratio')



import django_rq
from random import random

#  Utils

def didOccur(probability):
    """Return true if the event did occur, false otherwise"""

    return random() < probability

#  Methods

def oddsRatio(a, b, l):
    """
    Args:
        a: float
        b: float
        l: float

    Returns:
        Odds of a given event occurring based on a stat:
            Odds = stat(playerA) * stat(playerB) / stat(LeagueAvg)

    """

    return a*b/l


#  Indicators

def pitcher_contact_rate(pitcher):
    """Get contact rate for a pitcher.  Calculation includes fouls."""

    return pitcher['H'] / league_avg['H']


def batter_contact_rate(batter):
    """Get contact rate for a batter.  Calculation includes fouls."""

    return (batter['AB'] - batter['K']) / (league_avg['AB'] - league_avg['K'])

def league_contact_rate(league):
    return ()


def runPitch(pitcher, batter, league, method=oddsRatio):

    #  Was there contact?  Base this on Contact rate(ct%): ((AB - K) / AB) and the foul chance

    if(didOccur(
            method(batter_contact_rate(batter), pitcher_contact_rate(pitcher), contact_rate(league)))):
        print 'Made contact!'

import os
import csv
import datetime
from baseball.models import Player
from baseball.models import Stat
from datetime import date
import random

lahman_data = {}
players = []


for filename in os.listdir('baseball/resources/lahman/'):
    with open('baseball/resources/lahman/%s' % filename) as f:
        lahman_data[filename] = [line for line in csv.reader(f)]
        print 'Loaded %s' % filename


# class Player():
#     def __init__(self):
#         self.stats = {}
#     pass


# def foundPlayer(player, players):
#     return player in [p.stats['Master']['playerID'] for p in players]

def intorblank(num):
    if num == '':
        return 0
    else:
        return int(num)

def load(playername='', loadfrom='lahman'):

    masterheaders = lahman_data['Master.csv'][0]

    if loadfrom == 'lahman':
        print 'trying to load %s from lahman' % playername
        if not playername in [line[0] for line in lahman_data['Master.csv']]:
            print 'player not found'
        else:
            # if not foundPlayer(playername, players):
            playerrow = [row for row in lahman_data['Master.csv'] if row[0] == playername][0]
            print 'creating new player: %s %s' % (playerrow[masterheaders.index('nameGiven')], playerrow[masterheaders.index('nameLast')])

            #  Separate the first and middle names
            name_given = playerrow[masterheaders.index('nameFirst')].split(' ', 1)
            name_first = name_given[0]
            if len(name_given) > 1:
                name_middle = name_given[1]
            else:
                name_middle = ''

            #  Add the player
            player = Player(
                player_id=playerrow[masterheaders.index('playerID')],
                first_name=name_first,
                middle_name=name_middle,
                last_name=playerrow[masterheaders.index('nameLast')],
                nick_name=playerrow[masterheaders.index('nameFirst')],
                birth_country=playerrow[masterheaders.index('birthCountry')],
                birth_state=playerrow[masterheaders.index('birthState')],
                birth_city=playerrow[masterheaders.index('birthCity')],
                death_country=playerrow[masterheaders.index('deathCountry')],
                death_state=playerrow[masterheaders.index('deathState')],
                death_city=playerrow[masterheaders.index('deathCity')],
                weight=intorblank(playerrow[masterheaders.index('weight')]),
                height=intorblank(playerrow[masterheaders.index('height')]),
                bats=playerrow[masterheaders.index('bats')],
                throws=playerrow[masterheaders.index('throws')],
                retro_id=playerrow[masterheaders.index('retroID')],
                bbref_id=playerrow[masterheaders.index('bbrefID')]
            )

            #  Dates are sometimes blank, so handle that here
            def date_to_datetime(d):
                return datetime.datetime.combine(d, datetime.datetime.min.time())
            if playerrow[masterheaders.index('birthYear')]:
                #  Sometimes there is a year but no month/day
                if playerrow[masterheaders.index('birthMonth')] and playerrow[masterheaders.index('birthDay')]:
                    player.birth_date = date_to_datetime(date(int(playerrow[masterheaders.index('birthYear')]), int(playerrow[masterheaders.index('birthMonth')]), int(playerrow[masterheaders.index('birthDay')])))
                else:
                    player.birth_date = date_to_datetime(date(int(playerrow[masterheaders.index('birthYear')]), 1, 1))
            if playerrow[masterheaders.index('deathYear')]:
                if playerrow[masterheaders.index('deathMonth')] and playerrow[masterheaders.index('deathDay')]:
                    player.death_date = date_to_datetime(date(int(playerrow[masterheaders.index('deathYear')]), int(playerrow[masterheaders.index('deathMonth')]), int(playerrow[masterheaders.index('deathDay')])))
                else:
                    player.death_date = date_to_datetime(date(int(playerrow[masterheaders.index('deathYear')]), 1, 1))
            if playerrow[masterheaders.index('debut')]:
                player.debut = datetime.datetime.strptime(playerrow[masterheaders.index('debut')], '%Y-%m-%d').date()
            if playerrow[masterheaders.index('finalGame')]:
                player.final_game = datetime.datetime.strptime(playerrow[masterheaders.index('finalGame')], '%Y-%m-%d').date()

            player.save()


            #  Add the stats
            #  Batting
            battingheaders = lahman_data['Batting.csv'][0]
            if not playername in [line[0] for line in lahman_data['Batting.csv']]:
                print 'No batting stats found for %s.  Skipping.' %playername
            else:
                playerrow = [row for row in lahman_data['Batting.csv'] if row[0] == playername][0]
                for statname in battingheaders[2:]:

                    stat = Stat(
                        player=player,
                        date=date_to_datetime(date(int(playerrow[battingheaders.index('yearID')]), 1, 1)),
                        category='Batting',
                        name=statname,
                        abbr=statname,
                        value_str=str(playerrow[battingheaders.index(statname)]),
                    )
                    if statname in ['teamID', 'lgID'] or playerrow[battingheaders.index(statname)] == '':
                        value = 0
                    else:
                        value = intorblank(playerrow[battingheaders.index(statname)])
                    stat.value = value

                    stat.save()

                    player.stats.add(stat)
                    player.save()

            #  Appearances
            appheaders = lahman_data['Appearances.csv'][0]
            if not playername in [line[3] for line in lahman_data['Appearances.csv']]:
                print 'No appearances stats found for %s.  Skipping.' %playername
            else:
                playerrow = [row for row in lahman_data['Appearances.csv'] if row[3] == playername][0]
                for statname in appheaders[2:]:

                    stat = Stat(
                        player=player,
                        date=date_to_datetime(date(int(playerrow[appheaders.index('yearID')]), 1, 1)),
                        category='Appearances',
                        name=statname,
                        abbr=statname,
                        value_str=str(playerrow[appheaders.index(statname)]),
                        league=str(playerrow[appheaders.index('lgID')])
                    )
                    if statname in ['teamID', 'lgID', 'playerID'] or playerrow[appheaders.index(statname)] == '':
                        value = 0
                    else:
                        value = intorblank(playerrow[appheaders.index(statname)])
                    stat.value = value

                    stat.save()

                    player.stats.add(stat)
                    player.save()

            #  Fielding
            appheaders = lahman_data['Fielding.csv'][0]
            if not playername in [line[0] for line in lahman_data['Fielding.csv']]:
                print 'No Fielding stats found for %s.  Skipping.' %playername
            else:
                playerrow = [row for row in lahman_data['Fielding.csv'] if row[0] == playername][0]
                for statname in appheaders[1:]:

                    stat = Stat(
                        player=player,
                        date=date_to_datetime(date(int(playerrow[appheaders.index('yearID')]), 1, 1)),
                        category='Fielding',
                        name=statname,
                        abbr=statname,
                        value_str=str(playerrow[appheaders.index(statname)]),
                        league=str(playerrow[appheaders.index('lgID')])
                    )
                    if statname in ['teamID', 'lgID', 'playerID', 'POS'] or playerrow[appheaders.index(statname)] == '':
                        value = 0
                    else:
                        value = intorblank(playerrow[appheaders.index(statname)])
                    stat.value = value

                    stat.save()

                    player.stats.add(stat)
                    player.save()

            #  FieldingOF
            appheaders = lahman_data['FieldingOF.csv'][0]
            if not playername in [line[0] for line in lahman_data['FieldingOF.csv']]:
                print 'No FieldingOF stats found for %s.  Skipping.' %playername
            else:
                playerrow = [row for row in lahman_data['FieldingOF.csv'] if row[0] == playername][0]
                for statname in appheaders[1:]:

                    stat = Stat(
                        player=player,
                        date=date_to_datetime(date(int(playerrow[appheaders.index('yearID')]), 1, 1)),
                        category='FieldingOF',
                        name=statname,
                        abbr=statname,
                        value_str=str(playerrow[appheaders.index(statname)]),
                        league='N/A'
                    )
                    if statname in ['teamID', 'playerID'] or playerrow[appheaders.index(statname)] == '':
                        value = 0
                    else:
                        value = intorblank(playerrow[appheaders.index(statname)])
                    stat.value = value

                    stat.save()

                    player.stats.add(stat)
                    player.save()

            #  Pitching
            appheaders = lahman_data['Pitching.csv'][0]
            if not playername in [line[0] for line in lahman_data['Pitching.csv']]:
                print 'No Pitching stats found for %s.  Skipping.' %playername
            else:
                playerrow = [row for row in lahman_data['Pitching.csv'] if row[0] == playername][0]
                for statname in appheaders[1:]:

                    stat = Stat(
                        player=player,
                        date=date_to_datetime(date(int(playerrow[appheaders.index('yearID')]), 1, 1)),
                        category='Pitching',
                        name=statname,
                        abbr=statname,
                        value_str=str(playerrow[appheaders.index(statname)]),
                        league=str(playerrow[appheaders.index('lgID')])
                    )
                    if statname in ['teamID', 'lgID', 'playerID', 'POS'] or playerrow[appheaders.index(statname)] == '':
                        value = 0
                    else:
                        value = float(playerrow[appheaders.index(statname)])
                    stat.value = value

                    stat.save()

                    player.stats.add(stat)
                    player.save()

        # else:
        #     print 'updating existing player: %s %s' % [(row[masterheaders.index('nameGiven')], row[masterheaders.index('nameLast')]) for row in lahman_data['Master.csv'] if row[0] == playername][0]
        #     player = [p for p in players if p.stats['Master']['playerID'] == playername][0]

    #     for filename in lahman_data.keys():
    #         colheaders = lahman_data[filename][0]
    #         if not colheaders[0] == 'playerID':
    #             print 'skipping %s, it is not indexed by "player" but by "%s"' % (filename, colheaders[0])
    #         elif playername not in [i[0] for i in lahman_data[filename]]:
    #             print 'skipping %s, %s has no data there' % (filename, playername)
    #         else:
    #             stat_type = filename.replace('.csv', '')
    #             #player.stats[[stat_type] = {}
    #             for stat in colheaders:
    #                 print 'using stat type %s' % stat_type
    #                 player.stats[stat_type][stat] = [row[colheaders.index(stat)] for row in lahman_data[filename] if row[0] == playername][0]
    #                 #row[masterheaders.index('nameLast')]) for row in lahman_data['Master.csv'] if row[0] == playername][0]
    #     players.append(player)
    #     return player
    # else:
    #     print 'don\'t know how to load from "%s"!' % loadfrom

all_players = [line[0] for line in lahman_data['Master.csv'][1:]]
some_batters = [random.choice([line[0] for line in lahman_data['Batting.csv'][1:]]) for i in range(10)]
some_pitchers = [random.choice([line[0] for line in lahman_data['Pitching.csv'][1:]]) for i in range(10)]

# for player in (some_batters + some_pitchers):
#     load(player)
# asdf = load('adamsji01')

# for player in (all_players):
#     load(player)

# import ipdb
# ipdb.set_trace()
import pandas
import random
import csv
import os

_predicted_contestants = ['Spain', 'Russia', 'Portugal', 'Kazakhstan', 'Serbia', 'Croatia', 'Lithuania', 'Solomon Islands', 'Venezuela', 'Brazil', 'Paraguay',
                          'Argentina', 'Panama', 'Guatemala', 'United States', 'Costa Rica', 'China', 'Iran', 'Thailand', 'Saudi Arabia', 'Japan', 'Angola', 'Egypt', 'Morocco']

_scraped_results_path = 'scraped-data/FIFA_games.csv'
_scraped_groups_path = 'scraped-data/FIFA_groups.csv'
_preprocessed_data_path = 'preprocessed-data/data.csv'
_preprocessed_groups_path = 'preprocessed-data/groups.csv'


def initResults():
    global totalGamesByYear
    totalGamesByYear = 0
    global totalHomeGoals
    totalHomeGoals = 0
    global totalAwayGoals
    totalAwayGoals = 0
    global totalGoals
    totalGoals = 0
    global teamResults
    teamResults = {}


def updateTeamResults(teamResults, home, away, homeGoals, awayGoals):
    if (home not in teamResults):
        homeResults = [0, 0, 0, 0, 0, 0, 0]
    else:
        homeResults = teamResults[home]
    if (away not in teamResults):
        awayResults = [0, 0, 0, 0, 0, 0, 0]
    else:
        awayResults = teamResults[away]

    homeResults[0] += 1  # played
    homeResults[1] += 1 if homeGoals > awayGoals else 0  # won
    homeResults[2] += 1 if homeGoals < awayGoals else 0  # lost
    homeResults[3] += 1 if homeGoals == awayGoals else 0  # draw
    homeResults[4] += homeGoals  # gf
    homeResults[5] += awayGoals  # ga
    homeResults[6] += (homeGoals - awayGoals)  # gd

    awayResults[0] += 1  # played
    awayResults[1] += 1 if homeGoals < awayGoals else 0  # won
    awayResults[2] += 1 if homeGoals > awayGoals else 0  # lost
    awayResults[3] += 1 if homeGoals == awayGoals else 0  # draw
    awayResults[4] += awayGoals  # gf
    awayResults[5] += homeGoals  # ga
    awayResults[6] += (awayGoals - homeGoals)  # gd

    teamResults[home] = homeResults
    teamResults[away] = awayResults


if os.path.exists(_preprocessed_data_path):
    os.remove(_preprocessed_data_path)
if os.path.exists(_preprocessed_groups_path):
    os.remove(_preprocessed_groups_path)

initResults()

scraped_results = csv.reader(open(_scraped_results_path, encoding='UTF-8'))
scraped_groups = csv.reader(open(_scraped_groups_path, encoding='UTF-8'))
preprocessed_results = csv.writer(
    open(_preprocessed_data_path, mode='a', encoding='UTF-8', newline=''))
preprocessed_groups = csv.writer(
    open(_preprocessed_groups_path, mode='a', encoding='UTF-8', newline=''))

scraped_data_list = list(scraped_results)
scraped_groups_list = list(scraped_groups)


def writeResultsToCsv(year, host, numberOfTeams, totalGamesByYear, totalHomeGoals, totalAwayGoals, totalGoals, teamResult):
    preprocessed_results.writerow(
        ['', 'Year', 'Host', 'Total teams', 'Total games', 'Home goals', 'Away goals', 'Total goals'])
    preprocessed_results.writerow(
        ['', year, host, numberOfTeams, totalGamesByYear, totalHomeGoals, totalAwayGoals, totalGoals])
    preprocessed_results.writerow(
        ['Team', 'P', 'W', 'L', 'D', 'GF', 'GA', 'GD'])
    for key in teamResults.keys():
        teamResult = []
        teamResult.insert(0, key)
        teamResult += (teamResults[key])
        preprocessed_results.writerow(teamResult)


# Prepare world cup results for prediction
currentRowIndex = 0
for row in scraped_data_list:
    if (len(row) > 3):  # game rows have 5 cells
        gameResult = (row[3]).split('–')
        if ('-' in row[3]):
            gameResult = row[3].split('-')

        homeGoals = int(gameResult[0])
        awayGoals = int(gameResult[1])

        updateTeamResults(teamResults, row[2], row[4], homeGoals, awayGoals)

        totalGamesByYear += 1
        totalHomeGoals += homeGoals
        totalAwayGoals += awayGoals
        totalGoals += homeGoals + awayGoals
    elif (len(row) == 3 and totalGamesByYear != 0):  # if next year competition results start
        year = scraped_data_list[currentRowIndex -
                                 (totalGamesByYear+1)][1]  # get current year
        host = scraped_data_list[currentRowIndex -
                                 (totalGamesByYear+1)][2]  # get host
        numberOfTeams = len(teamResults)
        writeResultsToCsv(year, host, numberOfTeams, totalGamesByYear, totalHomeGoals,
                          totalAwayGoals, totalGoals, teamResults)  # write results
        initResults()  # restart results for next years cup
    currentRowIndex += 1

year = 0
num_teams = 0


def writeGroupsToCsv(num_groups, group_size, num_teams, col):
    max_number_of_teams = num_groups*group_size-1
    if(row[col] == 'Team' and num_teams % group_size == 0 and num_teams <= max_number_of_teams):
        preprocessed_groups.writerow([row[col]])
    elif(row[col] != 'Team' and num_teams <= max_number_of_teams):
        num_teams += 1
        preprocessed_groups.writerow([row[col]])

    return num_teams

# returns contestants split in equal groups by size (defined by groupSize)
def getGroups(contestants, groupSize):
    return [contestants[i:i + groupSize] for i in range(0, len(contestants), groupSize)]

for row in scraped_groups_list:
    if (len(row) == 1):
        year = int(row[0].split(' ')[0])
        if (year >= 2020):
            break
        preprocessed_groups.writerow(['Year', year])
        num_teams = 0

    if (1989 <= year <= 2004 and not len(row) == 1):
        # 4 groups of 4 teams
        num_teams = writeGroupsToCsv(4, 4, num_teams, 0)

    if (year == 2008 and not len(row) == 1):
        # 4 groups of 5 teams
        num_teams = writeGroupsToCsv(4, 5, num_teams, 0)

    if(year == 2012 and not len(row) == 1):
        # 6 groups of 4 teams
        num_teams = writeGroupsToCsv(6, 4, num_teams, 0)

    if(year == 2016 and not len(row) == 1):
        # 6 groups of 4 teams
        num_teams = writeGroupsToCsv(6, 4, num_teams, 1)

preprocessed_groups.writerow(['Year', 2020])
random.shuffle(_predicted_contestants)
random.shuffle(_predicted_contestants)
predictedGroups = getGroups(_predicted_contestants, 4)
for group in predictedGroups:
    preprocessed_groups.writerow(['Team', ''])
    for team in group:
        preprocessed_groups.writerow([team, ''])
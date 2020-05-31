import csv
from pprint import pprint
import itertools 
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import poisson, skellam

# returns historical results of teams, excluding the year which will be predicted
# n (18|22|26) - number of rows in csv file, in which the countries(teams) are written to, devided by year
def getHistoricalResults(excludeYear, n):
    with open('preprocessed-data/data.csv', encoding='UTF-8') as results:
        rowsToDrop = []
        for row_num, row in enumerate(csv.reader(results, delimiter=',')):
            if len(row) > 0:
                strRow = str(row)
                if "['', 'Year', 'Host', 'Total teams', 'Total games', 'Home goals', 'Away goals', 'Total goals']" in strRow:
                    rowsToDrop.append(row_num)
                if "['Team', 'P', 'W', 'L', 'D', 'GF', 'GA', 'GD']" in strRow:
                    rowsToDrop.append(row_num)
                if "['', " in strRow:
                    rowsToDrop.append(row_num)
                if "['', '"+str(excludeYear)+"', " in strRow:
                    for i in range(0, n):
                        rowsToDrop.append(row_num+i)

        header=['Team','P', 'W', 'L', 'D', 'GF', 'GA', 'GD']
        df = pd.read_csv('preprocessed-data/data.csv', skiprows=rowsToDrop, names=header)
        aggregation_functions = {'P': 'sum', 'W': 'sum', 'L': 'sum', 'D': 'sum', 'GF': 'sum', 'GA': 'sum', 'GD': 'sum'} 
        # sums all team results by columns, except results of the excluded year, which is being predicted
        teams = df.groupby(df['Team']).aggregate(aggregation_functions)
        # creates dictionary, where key is country(team) name, and value is list of teams historical results 
        teams_dict = {key:row.tolist() for key,row in teams.iterrows()} 
    return teams_dict

# n (21|25|31) - number of rows in csv file, in which the contestants are written to, devided by year
def getContestants(year, n):
    with open('preprocessed-data/groups.csv', encoding='UTF-8') as groups:
        rowsToKeep = []
        for row_num, row in enumerate(csv.reader(groups, delimiter=',')):
            if "['Year', '"+str(year)+"']" in str(row):
                    for i in range(0, n):
                        rowsToKeep.append(row_num+i)
        
        pred = lambda x: x not in rowsToKeep
        header=['Team', '']
        df = pd.read_csv('preprocessed-data/groups.csv', skiprows=pred, names=header)
        contestants = df['Team'].tolist()
        contestants = list(filter(lambda x: x != 'Team' and x!='Year', contestants))
    return contestants

# returns contestants split in equal groups by size (defined by groupSize)
def getGroups(contestants, groupSize):
    return [contestants[i:i + groupSize] for i in range(0, len(contestants), groupSize)]

# returns matches by group, one game between teams, TODO: (it's not important which team is home/away ...)
def getMatches(group):
    return list(itertools.combinations(group, 2))

def getAvgerageGoals(teamName):
    if teamName in historicalResults.keys():
        teamResults = historicalResults[teamName]
        return teamResults[4]/teamResults[0]
    else:
        return 1.2 # debutant team, guess for goals average, fixed 

def getHomeWinsChances(match):
    return np.sum(np.tril(match, -1))

def getDrawChances(match):
    return np.sum(np.diag(match))

def getAwayWinsChances(match):
    return np.sum(np.triu(match, 1))

def simulateMatch(homeTeam, awayTeam, max_goals=15):
    home_goals_avg = getAvgerageGoals(homeTeam)
    away_goals_avg = getAvgerageGoals(awayTeam)
    prediction = [[poisson.pmf(i, team_avg) for i in range(0, max_goals+1)] for team_avg in [home_goals_avg, away_goals_avg]]
    return (np.outer(np.array(prediction[0]), np.array(prediction[1])))

def printPredictionResults(homeTeam, awayTeam, match, index):
    print('\n' + str(index))
    pprint(homeTeam + " chances to win: " + str(getHomeWinsChances(match)))
    pprint(awayTeam + " chances to win: " + str(getAwayWinsChances(match)))
    pprint("Chances of draw: " + str(getDrawChances(match)))

def updateStandings(home, away, group, homePoints, awayPoints, standings):
    updateTeamStandings(home, group, homePoints, standings)
    updateTeamStandings(away, group, awayPoints, standings)
    return standings

def updateTeamStandings(team, group, points, standings):
    if team in standings.keys():
        entry = standings[team]
        new_points = entry[1] + points
        entry = {team: [group, new_points]}
    else:
        entry = {team: [group, points]}
    standings.update(entry)        
    return standings

def decideOutcome(home, away, group, match, standings):
    results = [getHomeWinsChances(match), getAwayWinsChances(match), getDrawChances(match)]
    result = results.index(max(results))
    if result == 0:
        updateStandings(home, away, group, 3, 0, standings)
    if result == 1:  
        updateStandings(home, away, group, 0, 3, standings)
    if result == 2:  
        updateStandings(home, away, group, 1, 1, standings)
    
    return standings

def getFirstNTeams(n, standings):
    sortedStandings = {k: v for k, v in sorted(standings.items(), key=lambda item: item[1][1], reverse=True)}
    t = [*sortedStandings]
    return t[:n]

def knockoutStageMatches(teams):
    randomOrderTeams = teams
    random.shuffle(randomOrderTeams)
    matches = getGroups(randomOrderTeams, 2)
    return matches

# crosswise selection (by placement) of teams from first stage groups
def createSecondStageGroups(teams):
    group1 = [teams[0], teams[3], teams[4], teams[7]] # 1 4 5 8
    group2 = [teams[1], teams[2], teams[5], teams[6]] # 2 3 6 7
    return [group1, group2]

# crosswise selection (by placement) of teams from second stage groups
def getSemifinalists(teams):
    semifinals1 = [teams[0], teams[3]] # 1 4
    semifinals2 = [teams[1], teams[2]] # 2 3
    return [semifinals1, semifinals2]

def get3rdPlaceMatch(teams):
    return [teams[2], teams[3]] # 3vs4

def getFinalists(teams):
    return [teams[0], teams[1]] # 1vs2

def stageSimulation(groups, n):
    standings = {}
    for j in range(0, len(groups)):
        matches = getMatches(groups[j])
        for i in range(0, len(matches)):
            home = matches[i][0]
            away = matches[i][1]
            match = simulateMatch(home, away, 15)
            standings = decideOutcome(home, away, j, match, standings)
    pprint(standings)

    progressingToNextStage = getFirstNTeams(n, standings)
    pprint(progressingToNextStage) # best of n, which are going to next round
    return progressingToNextStage

year = 2020

hrrows = 0
crows = 0
nteams = 0

if ( 1989 <= year <= 2004):
    hrrows = 18
    crows = 21
    nteams = 4
if ( year == 2008):
    hrrows = 22
    crows = 25
    nteams = 5
if ( 2012 <= year <= 2021): 
    hrrows = 26
    crows = 31
    nteams = 4
    
historicalResults = getHistoricalResults(year, hrrows)
contestants = getContestants(year, crows)
groups = getGroups(contestants, nteams)
# pprint(historicalResults)

# model1: stage1, stage2, semifinals - 1989-2008
if ( 1989 <= year <= 2008):
    progressingToNextStage = stageSimulation(groups, 8)
    groups = createSecondStageGroups(progressingToNextStage)
    progressingToNextStage = stageSimulation(groups, 4)
    groups = getSemifinalists(progressingToNextStage)
    progressingToNextStage = stageSimulation(groups, 4)

# model2: stage1, knockout stage - 2012-2021
if (2012 <= year <= 2021):
    progressingToNextStage = stageSimulation(groups, 16)
    matches = knockoutStageMatches(progressingToNextStage)
    progressingToNextStage = stageSimulation(matches, 8)
    matches = knockoutStageMatches(progressingToNextStage)
    progressingToNextStage = stageSimulation(matches, 4)

# finals
finalsMatch = getFinalists(progressingToNextStage)
thirdPlaceMatch = get3rdPlaceMatch(progressingToNextStage)
finals = stageSimulation([thirdPlaceMatch, finalsMatch], 4)
winner = finals[1]
secondPlace = finals[3]
thirdPlace = finals[0]
fourthPlace = finals[2]
pprint("1st: " + winner)
pprint("2nd: " + secondPlace)
pprint("3rd: " + thirdPlace)
pprint("4th: " + fourthPlace)
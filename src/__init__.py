#!/bin/env python3

import sys
import requests
import getpass
import argparse
import os
import json
import glob
import base64

from src.teams import Team, getTeamCoefficientAverage, getTeamPoints

from .lines import parseFile

TEAM_JSON = 'teams.json'
IN_DIR = 'in'


def download():
    eventId = input('Event ID: ')
    username = input('FKSDB Username: ')
    password = getpass.getpass('FKSDB password: ')

    print(f"Downloading teams data for event {eventId}")

    req = get_teams(eventId, username, password)

    print("Saving")

    with open(TEAM_JSON, 'wb') as jsonFile:
        jsonFile.write(req.content)

    print("Download complete")

def get_teams(eventId, username, password):
    credentials = f"{username}:{password}".encode("utf-8")
    encoded_credentials = base64.b64encode(credentials).decode("utf-8")
    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    req = requests.get(
        f'https://db.fykos.cz/api/events/{eventId}/teams',
        headers=headers
    )
    return req


def printTeamTable(teams):
    titleString = f"│ N │{"Nátev týmu":32}│{"ID":^5}│Kat.│Body│Poř. glob.|Poř. v kat.|"
    print("—"*len(titleString))
    print(titleString)
    print("—"*len(titleString))
    for i in range(len(teams)):
        team = teams[i]
        print(
            f"│{i+1:>3}│{team.name:<32}│{team.teamId:>5}│{team.category:^4}│{team.pointsSum:>4}│{team.rankTotal:>10}│{team.rankCategory:>11}│"
        )
    print("—"*len(titleString))


def process():
    # load teams
    if not os.path.exists(TEAM_JSON):
        print("Missing JSON data file of teams, please run download first")
        sys.exit()
    with open(TEAM_JSON, 'r') as jsonFile:
        teamsJsonData = json.load(jsonFile)

    # load in files
    if not os.path.exists(IN_DIR):
        print(f"Missing directory `{IN_DIR}` with input CSV files")
        sys.exit()
    if not os.path.isdir(IN_DIR):
        print(f"`{IN_DIR}` is not a directory")
        sys.exit()

    inputFiles = glob.glob(IN_DIR + "/*.csv")

    if (len(inputFiles) == 0):
        print("No input file found")
        sys.exit()

    teamTasks = {}
    for inputFile in inputFiles:
        parseFile(inputFile, teamTasks)

    teamPoints = getTeamPoints(teamTasks)

    teams = []
    for teamId in teamPoints:
        coeffAvg = getTeamCoefficientAverage(
            teamsJsonData[str(teamId)]['members'])
        teams.append(Team(
            teamId,
            teamsJsonData[str(teamId)]['name'],
            teamPoints[teamId],
            coeffAvg,
            teamsJsonData[str(teamId)]['category']
        ))

    # rank teams
    teamsA = sorted([team for team in teams.copy() if team.category == 'A'])
    teamsB = sorted([team for team in teams.copy() if team.category == 'B'])
    teamsC = sorted([team for team in teams.copy() if team.category == 'C'])
    teams.sort()

    # save team ranks
    for i in range(len(teams)):
        teams[i].rankTotal = i+1
    for group in [teamsA, teamsB, teamsC]:
        for i in range(len(group)):
            group[i].rankCategory = i+1

    # update original JSON data
    for team in teams:
        teamsJsonData[str(team.teamId)]['rankTotal'] = team.rankTotal
        teamsJsonData[str(team.teamId)]['rankCategory'] = team.rankCategory
        teamsJsonData[str(team.teamId)]['points'] = team.pointsSum
        teamsJsonData[str(team.teamId)]['state'] = 'participated'

    with open('teams-calculated.json', 'w') as file:
        json.dump(teamsJsonData, file)

    # print results
    print("\nTýmy seřazeny dle pořadí\n")
    print("Globální pořadí")
    printTeamTable(teams)
    print()
    print("Kategorie A")
    printTeamTable(teamsA)
    print()
    print("Kategorie B")
    printTeamTable(teamsB)
    print()
    print("Kategorie C")
    printTeamTable(teamsC)

    # print sorted by team name
    teamsByName = teams.copy()
    teamsByNameA = teamsA.copy()
    teamsByNameB = teamsB.copy()
    teamsByNameC = teamsC.copy()
    sorted(teamsByName, key=lambda team: team.name)
    sorted(teamsByNameA, key=lambda team: team.name)
    sorted(teamsByNameB, key=lambda team: team.name)
    sorted(teamsByNameC, key=lambda team: team.name)

    print("\nTýmy seřazeny dle názvu\n")
    print("Všechny týmy")
    printTeamTable(teams)
    print()
    print("Kategorie A")
    printTeamTable(teamsA)
    print()
    print("Kategorie B")
    printTeamTable(teamsB)
    print()
    print("Kategorie C")
    printTeamTable(teamsC)


def main():
    parser = argparse.ArgumentParser(
        description='systém pro spočítání bodů a pořadí týmů z CSV tabulek s kódy úloh a počtem bodů'
    )
    parser.set_defaults(func=process)

    subparsers = parser.add_subparsers(title='subcommands')
    downloadParser = subparsers.add_parser(
        'download',
        description='stáhnutí dat o týmech z FKSDB'
    )
    downloadParser.set_defaults(func=download)

    args = parser.parse_args()

    try:
        args.func()
    except KeyboardInterrupt:
        sys.exit()

#!/bin/env python3

import sys
import requests
import getpass
import argparse
import os
import json
import glob

from .lines import parseFile

TEAM_JSON = 'teams.json'
IN_DIR = 'in'


def download():
    eventId = input('Event ID: ')
    username = input('FKSDB Username: ')
    password = getpass.getpass('FKSDB password: ')

    print(f"Downloading teams data for event {eventId}")

    req = requests.get(
        f'https://db.fykos.cz/api/events/{eventId}/teams',
        auth=(username, password)
    )

    print("Saving")

    with open(TEAM_JSON, 'wb') as jsonFile:
        jsonFile.write(req.content)

    print("Download complete")


def process():
    # load teams
    if not os.path.exists(TEAM_JSON):
        print("Missing JSON data file of teams, please run download first")
        sys.exit()
    with open(TEAM_JSON, 'r') as jsonFile:
        teams = json.load(jsonFile)

    # load in files
    if not os.path.exists(IN_DIR):
        print(f"Missing directory `{IN_DIR}` with input CSV files")
        sys.exit()
    if not os.path.isdir(IN_DIR):
        print(f"`{IN_DIR}` is not a directory")
        sys.exit()

    inputFiles = glob.glob(IN_DIR + "/*.csv")
    print(inputFiles)

    if (len(inputFiles) == 0):
        print("No input files found")
        sys.exit()

    tasks = {}
    for inputFile in inputFiles:
        parseFile(inputFile, tasks)


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

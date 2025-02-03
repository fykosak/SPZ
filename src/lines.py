import re

from .teams import appendTeamsData
from .code import extractCodeData


class LineException(Exception):
    pass


def splitLine(line: str):
    # remove quotes
    line = line.replace('"', '')

    # swap any delimiter char with ;
    line = line.replace(',', ';').replace(' ', ';').replace('\t', ';')

    # remove duplicates
    line = re.sub(';+', ';', line)
    split = line.split(';')

    if (len(split) == 2):
        return (split[0], split[1])
    raise LineException(f"Could not extract data from line `{line}`")


def extractLineData(line: str):
    line = line.strip()
    split = splitLine(line)
    (code, points) = split
    (teamId, task) = extractCodeData(code)
    return (teamId, task, int(points))


def parseFile(inputFile: str, teamTasks: dict):
    with open(inputFile, 'r') as file:
        for line in file:
            (teamId, task, points) = extractLineData(line)
            appendTeamsData(teamId, task, points, teamTasks)

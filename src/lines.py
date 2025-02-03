import re

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
    if split is None:
        return None
    (code, points) = split
    print(f"Code: {code}")
    print(f"Points: {points}")
    extractCodeData(code)


def parseFile(inputFile, tasks):
    with open(inputFile, 'r') as file:
        for line in file:
            extractLineData(line)

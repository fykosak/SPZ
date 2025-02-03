class DuplicatePointsEntryException(Exception):
    def __init__(self, teamId, task) -> None:
        super().__init__(f"Duplicate points entry for team {teamId} \
                         for task {task} with different points.")


class InvalidPointsException(Exception):
    def __init__(self, points, teamId, task) -> None:
        super().__init__(
            f"Invalid points {points} for team {teamId} on task {task}")


class InvalidTaskException(Exception):
    def __init__(self, task, teamId) -> None:
        super().__init__(
            f"Invalid task {task} for team {teamId}")


def appendTeamsData(teamId: int, task: str, points: int, teamTasks: dict) -> None:
    # validate date before insersion
    if points not in [1, 2, 3, 5]:
        raise InvalidPointsException(points, teamId, task)

    if len(task) != 2:
        raise InvalidTaskException(task, teamId)

    if task[0] not in 'ABCDEFGH' or task[1] not in 'ABCDEFGH':
        raise InvalidTaskException(task, teamId)

    if not teamId in teamTasks:
        teamTasks[teamId] = {}

    if task in teamTasks[teamId]:  # if already present, then it's a duplicate
        # raise error if points are not the same
        if teamTasks[teamId][task] != points:
            raise DuplicatePointsEntryException(teamId, task)

    teamTasks[teamId][task] = points


def getTeamPoints(teamTasks: dict) -> dict:
    teamPoints = {}
    for teamId in teamTasks:
        pointsSum = 0
        pointsCount = {}
        for task in teamTasks[teamId]:
            points = teamTasks[teamId][task]
            pointsSum += points
            if points in pointsCount:
                pointsCount[points] += 1
            else:
                pointsCount[points] = 1
        teamPoints[teamId] = {
            'sum': pointsSum,
            'counts': pointsCount
        }
    return teamPoints


# def orderTeams(teamPoints: dict):
#    teams = []
#    for ()

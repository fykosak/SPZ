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
        super().__init__(f"Invalid task {task} for team {teamId}")


class InvalidStudyYearException(Exception):
    def __init__(self, studyYear) -> None:
        super().__init__(f"Invalid study year {studyYear}")


class Team:
    def __init__(self, teamId, points, coefficientAverage, category) -> None:
        self.teamId = teamId
        self.pointsSum = points['sum']
        self.pointsCounts = points['counts']
        self.coefficientAverage = coefficientAverage
        self.category = category

    def __repr__(self) -> str:
        return f"<{self.teamId}, {self.category}>"

    def __eq__(self, obj):
        return self.teamId == obj.teamId

    def __lt__(self, obj):
        if self.teamId == obj.teamId:
            return False
        # compare sum
        if self.pointsSum > obj.pointsSum:
            return True
        if self.pointsSum < obj.pointsSum:
            return False

        # compare averages -> sum is same, so compare counts
        if self.getTotalPointsCount() < obj.getTotalPointsCount():
            return True
        if self.getTotalPointsCount() > obj.getTotalPointsCount():
            return False

        # more 5 point submits
        if self.getPointsCount(5) > obj.getPointsCount(5):
            return True
        if self.getPointsCount(5) < obj.getPointsCount(5):
            return False

        # more 3 point submits
        if self.getPointsCount(3) > obj.getPointsCount(3):
            return True
        if self.getPointsCount(3) < obj.getPointsCount(3):
            return False

        # lower coefficient
        if self.coefficientAverage < obj.coefficientAverage:
            return True
        if self.coefficientAverage > obj.coefficientAverage:
            return False

        # lower team id
        if self.teamId < obj.teamId:
            return True

        return False

    def getTotalPointsCount(self) -> int:
        count = 0
        for points in self.pointsCounts:
            count += self.pointsCounts[points]
        return count

    def getPointsCount(self, point):
        if point in self.pointsCounts:
            return self.pointsCounts[point]
        return 0


def studyYearToCoefficient(studyYear: str):
    match studyYear:
        case 'H_1':
            return 1
        case 'H_2':
            return 2
        case 'H_3':
            return 3
        case 'H_4':
            return 4
        case 'U_ALL' | None:
            raise InvalidStudyYearException(studyYear)
        case _:
            return 0


def getTeamCoefficientAverage(members) -> float:
    memberCount = 0
    coeffSum = 0
    for member in members:
        memberCount += 1
        coeffSum += studyYearToCoefficient(member['studyYear'])
    return coeffSum/memberCount


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

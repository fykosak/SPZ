import pytest
import random

from src.teams import DuplicatePointsEntryException, InvalidPointsException, InvalidStudyYearException, InvalidTaskException, Team, appendTeamsData, getTeamCoefficientAverage, getTeamPoints, studyYearToCoefficient


def test_simple():
    teamTasks = {}
    appendTeamsData(1234, 'AA', 5, teamTasks)
    appendTeamsData(1234, 'BA', 3, teamTasks)
    appendTeamsData(1234, 'CD', 2, teamTasks)
    appendTeamsData(1234, 'EG', 1, teamTasks)
    appendTeamsData(1235, 'HA', 5, teamTasks)
    assert teamTasks == {
        1234: {
            'AA': 5,
            'BA': 3,
            'CD': 2,
            'EG': 1,
        },
        1235: {
            'HA': 5,
        }
    }


def test_duplicate_valid():
    teamTasks = {}
    appendTeamsData(1234, 'AA', 5, teamTasks)
    appendTeamsData(1234, 'BA', 3, teamTasks)
    appendTeamsData(1234, 'CD', 2, teamTasks)
    appendTeamsData(1234, 'AA', 5, teamTasks)
    appendTeamsData(1234, 'EG', 1, teamTasks)
    appendTeamsData(1235, 'HA', 5, teamTasks)
    assert teamTasks == {
        1234: {
            'AA': 5,
            'BA': 3,
            'CD': 2,
            'EG': 1,
        },
        1235: {
            'HA': 5,
        }
    }


def test_duplicate_invalid():
    teamTasks = {}
    appendTeamsData(1234, 'AA', 5, teamTasks)
    with pytest.raises(DuplicatePointsEntryException):
        appendTeamsData(1234, 'AA', 3, teamTasks)


def test_invalid_points():
    with pytest.raises(InvalidPointsException):
        appendTeamsData(1234, 'AA', 4, {})
    with pytest.raises(InvalidPointsException):
        appendTeamsData(1234, 'AA', 0, {})
    with pytest.raises(InvalidPointsException):
        appendTeamsData(1234, 'AA', -1, {})
    with pytest.raises(InvalidPointsException):
        appendTeamsData(1234, 'AA', 6, {})


def test_invalid_task():
    with pytest.raises(InvalidTaskException):
        appendTeamsData(1234, 'A', 5, {})
    with pytest.raises(InvalidTaskException):
        appendTeamsData(1234, 'AAA', 5, {})
    with pytest.raises(InvalidTaskException):
        appendTeamsData(1234, 'AI', 5, {})
    with pytest.raises(InvalidTaskException):
        appendTeamsData(1234, 'aa', 5, {})
    with pytest.raises(InvalidTaskException):
        appendTeamsData(1234, 'IA', 5, {})
    with pytest.raises(InvalidTaskException):
        appendTeamsData(1234, 'HI', 5, {})
    with pytest.raises(InvalidTaskException):
        appendTeamsData(1234, 'IH', 5, {})


def test_points_sum():
    teamTasks = {
        1234: {
            'AA': 5,
            'BA': 3,
            'BB': 3,
            'EG': 1,
        },
        1235: {
            'HA': 3,
        }
    }
    assert getTeamPoints(teamTasks) == {
        1234: {
            'sum': 12,
            'counts': {
                5: 1,
                3: 2,
                1: 1,
            }
        },
        1235: {
            'sum': 3,
            'counts': {
                3: 1
            }
        }
    }


def get_test_teams():
    return [
        Team(8, {'sum': 15, 'counts': {5: 3}}, 4, 'A'),
        Team(2, {'sum': 8, 'counts': {5: 1, 3: 1}}, 4, 'B'),
        Team(1, {'sum': 8, 'counts': {5: 1, 2: 1, 1: 1}}, 4, 'A'),
        Team(4, {'sum': 8, 'counts': {3: 2, 2: 1}}, 4, 'B'),
        Team(3, {'sum': 4, 'counts': {3: 1, 1: 1}}, 4, 'A'),
        Team(7, {'sum': 4, 'counts': {2: 2}}, 1, 'A'),
        Team(5, {'sum': 4, 'counts': {2: 2}}, 4, 'B'),
        Team(6, {'sum': 4, 'counts': {2: 2}}, 4, 'A')
    ]


def test_team_compare_eq():
    teams = get_test_teams()
    for i in range(0, len(teams)):
        assert teams[i] == teams[i]


def test_team_compare_gt():
    teams = get_test_teams()
    for i in range(0, 7):
        assert not teams[i] < teams[i]
        assert not teams[i] > teams[i]
        for j in range(i+1, 7+1):
            assert teams[i] < teams[j]
            assert not (teams[i] > teams[j])


def test_team_sort():
    teams = [
        Team(8, {'sum': 15, 'counts': {5: 3}}, 4, 'A'),
        Team(2, {'sum': 8, 'counts': {5: 1, 3: 1}}, 4, 'B'),
        Team(1, {'sum': 8, 'counts': {5: 1, 2: 1, 1: 1}}, 4, 'A'),
        Team(4, {'sum': 8, 'counts': {3: 2, 2: 1}}, 4, 'B'),
        Team(3, {'sum': 4, 'counts': {3: 1, 1: 1}}, 4, 'A'),
        Team(7, {'sum': 4, 'counts': {2: 2}}, 1, 'A'),
        Team(5, {'sum': 4, 'counts': {2: 2}}, 4, 'B'),
        Team(6, {'sum': 4, 'counts': {2: 2}}, 4, 'A')
    ]
    sorted(teams, key=lambda team: team.teamId)
    print(teams)
    assert teams[0].teamId == 8
    assert teams[1].teamId == 2
    assert teams[2].teamId == 1
    assert teams[3].teamId == 4
    assert teams[4].teamId == 3
    assert teams[5].teamId == 7
    assert teams[6].teamId == 5
    assert teams[7].teamId == 6


def test_study_year_to_coefficient():
    assert studyYearToCoefficient('H_1') == 1
    assert studyYearToCoefficient('H_2') == 2
    assert studyYearToCoefficient('H_3') == 3
    assert studyYearToCoefficient('H_4') == 4
    assert studyYearToCoefficient('P_9') == 0
    assert studyYearToCoefficient('P_8') == 0
    assert studyYearToCoefficient('P_7') == 0
    assert studyYearToCoefficient('P_6') == 0
    assert studyYearToCoefficient('P_5') == 0
    with pytest.raises(InvalidStudyYearException):
        studyYearToCoefficient('U_ALL')
    with pytest.raises(InvalidStudyYearException):
        studyYearToCoefficient(None)


def test_team_coefficient_average():
    assert getTeamCoefficientAverage([{'studyYear': 'H_1'}]) == 1
    assert getTeamCoefficientAverage(
        [{'studyYear': 'H_2'}, {'studyYear': 'H_3'}]
    ) == 2.5
    assert getTeamCoefficientAverage(
        [{'studyYear': 'H_1'}, {'studyYear': 'H_2'}, {'studyYear': 'H_3'}]
    ) == 2
    assert getTeamCoefficientAverage(
        [{'studyYear': 'H_1'}, {'studyYear': 'H_3'}, {'studyYear': 'H_3'}]
    ) == 7/3
    assert getTeamCoefficientAverage(
        [{'studyYear': 'P_9'}, {'studyYear': 'H_4'}]
    ) == 2

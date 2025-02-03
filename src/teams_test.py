import pytest

from src.teams import DuplicatePointsEntryException, InvalidPointsException, InvalidTaskException, appendTeamsData, getTeamPoints


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

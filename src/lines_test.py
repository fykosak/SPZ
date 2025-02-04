from src.lines import LineException, extractLineData, parseFile, splitLine

import pytest


def test_split():
    assert splitLine('1234AA1;5') == ('1234AA1', '5')
    assert splitLine('1234AA1,3') == ('1234AA1', '3')
    assert splitLine('1234AA1 2') == ('1234AA1', '2')
    assert splitLine('1234AA1\t1') == ('1234AA1', '1')


def test_split_multiple():
    assert splitLine('1234AA1;;;5') == ('1234AA1', '5')
    assert splitLine('1234AA1,,,3') == ('1234AA1', '3')
    assert splitLine('1234AA1;,;2') == ('1234AA1', '2')
    assert splitLine('1234AA1 , 1') == ('1234AA1', '1')
    assert splitLine('1234AA1\t\t5') == ('1234AA1', '5')


def test_quotes():
    assert splitLine('"1234AA1";5') == ('1234AA1', '5')
    assert splitLine('1234AA1,"5"') == ('1234AA1', '5')
    assert splitLine('"1234AA1" "5"') == ('1234AA1', '5')
    assert splitLine('"1234AA1\t5"') == ('1234AA1', '5')


def test_extract():
    assert extractLineData('001234AA8;5\n') == (1234, 'AA', 5)
    assert extractLineData('012345BC2;3\n') == (12345, 'BC', 3)


def test_invalid():
    with pytest.raises(LineException):
        splitLine("001234AA8;5;5")
    with pytest.raises(LineException):
        splitLine("001234AA8")


@pytest.fixture(scope="session")
def input_file(tmp_path_factory):
    contents = "001234AA8;5\n012345BC2;3\n1234AB1;,;2"
    fn = tmp_path_factory.mktemp("data") / "test.csv"
    with open(fn, 'w') as file:
        file.write(contents)
    return fn


def test_file_parsing(input_file):
    teamTask = {}
    parseFile(input_file, teamTask)
    assert teamTask == {
        1234: {
            'AA': 5,
            'AB': 2,
        },
        12345: {
            'BC': 3,
        }
    }

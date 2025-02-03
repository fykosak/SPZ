from src.lines import extractLineData, splitLine


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

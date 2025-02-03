from src.lines import splitLine


def test_split():
    assert splitLine('1234AA1;5') == ('1234AA1', '5')
    assert splitLine('1234AA1,5') == ('1234AA1', '5')
    assert splitLine('1234AA1 5') == ('1234AA1', '5')
    assert splitLine('1234AA1\t5') == ('1234AA1', '5')


def test_split_multiple():
    assert splitLine('1234AA1;;;5') == ('1234AA1', '5')
    assert splitLine('1234AA1,,,5') == ('1234AA1', '5')
    assert splitLine('1234AA1;,;5') == ('1234AA1', '5')
    assert splitLine('1234AA1 , 5') == ('1234AA1', '5')
    assert splitLine('1234AA1\t\t5') == ('1234AA1', '5')


def test_quotes():
    assert splitLine('"1234AA1";5') == ('1234AA1', '5')
    assert splitLine('1234AA1,"5"') == ('1234AA1', '5')
    assert splitLine('"1234AA1" "5"') == ('1234AA1', '5')
    assert splitLine('"1234AA1\t5"') == ('1234AA1', '5')

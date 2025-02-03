#!/bin/env python3

import pytest

from .code import CodeChecksumException, CodeTooShortException, InvalidCodeLengthException, extractCodeData, verifyCode


def test_valid():
    verifyCode('001234AA8')
    verifyCode('001234AB1')
    verifyCode('001235BC0')
    verifyCode('012356AH2')
    verifyCode('012356HH1')
    verifyCode('482923HH6')


def test_invalid():
    with pytest.raises(CodeChecksumException):
        verifyCode('001234AA9')
    with pytest.raises(CodeChecksumException):
        verifyCode('012345HH2')
    with pytest.raises(CodeChecksumException):
        verifyCode('482923HH2')


def test_extract():
    assert extractCodeData('001234AA8') == (1234, 'AA')
    assert extractCodeData('1234AA8') == (1234, 'AA')
    assert extractCodeData('001234AB1') == (1234, 'AB')
    assert extractCodeData('001235BC0') == (1235, 'BC')
    assert extractCodeData('012356AH2') == (12356, 'AH')
    assert extractCodeData('012356HH1') == (12356, 'HH')


def test_short():
    with pytest.raises(InvalidCodeLengthException):
        verifyCode('01234AA9')
    with pytest.raises(InvalidCodeLengthException):
        verifyCode('AA9')
    with pytest.raises(CodeTooShortException):
        extractCodeData('AA9')

class CodeException(Exception):
    pass


class CodeChecksumException(CodeException):
    def __init__(self, code) -> None:
        super().__init__(f"Invalid checksum in code {code}")


class InvalidCodeLengthException(CodeException):
    def __init__(self, code) -> None:
        super().__init__(f"Invalid length of {code}")


class CodeTooShortException(CodeException):
    def __init__(self, code) -> None:
        super().__init__(f"Code {code} too short")


def verifyCode(code: str):
    intcode = code.replace('A', '1').replace('B', '2').replace('C', '3').replace('D', '4')\
        .replace('E', '5').replace('F', '6').replace('G', '7').replace('H', '8').replace('X', '0')
    if len(intcode) != 9:
        raise InvalidCodeLengthException(code)
    controlSum = 3*(int(intcode[0]) + int(intcode[3]) + int(intcode[6])) \
        + 7 * (int(intcode[1]) + int(intcode[4]) + int(intcode[7])) \
        + int(intcode[2]) + int(intcode[5]) + int(intcode[8])
    if (controlSum % 10 != 0):
        raise CodeChecksumException(code)


def extractCodeData(code: str):
    # check that code has at least 1 team digit, 2 task chars and control sum
    if len(code) < 5:
        raise CodeTooShortException(code)

    # pad code to 9 chars
    code = '0'*(9-len(code)) + code.upper()

    teamId = int(code[0:5+1])
    task = code[6:7+1]
    verifyCode(code)
    return (teamId, task)

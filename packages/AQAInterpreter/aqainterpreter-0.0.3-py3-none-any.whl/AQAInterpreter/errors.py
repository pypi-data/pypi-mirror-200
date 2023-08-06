from AQAInterpreter.tokens import *
from dataclasses import dataclass
import sys

@dataclass
class AQARuntimeError(RuntimeError):
    token: Token
    message: str

class AQAParseError(AQARuntimeError): ...

def report(line: int, where: str, message: str) -> None:
    print(f"[line {line}] Error {where}: {message}", file=sys.stderr)


def error(token: Token | int, message: str) -> None:
    if isinstance(token, Token):
        if token.type == NEWLINE:
            report(token.line, "at end of line", message)
        else:
            report(token.line, " at '" + token.lexeme + "'", message)
    else:
        line = token
        report(line, "", message)
    had_error = True
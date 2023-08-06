from AQAInterpreter.tokens import *
from AQAInterpreter import errors


@dataclass
class Scanner:
    source: str
    _start: int = 0
    _current: int = 0
    _line: int = 1
    _tokens: list[Token] = field(default_factory=list)

    def _at_end(self) -> bool:
        return self._current >= len(self.source)

    def _add(self, token_type: str, literal: str | None = None) -> None:
        self._tokens.append(
            Token(
                token_type,
                literal=literal,
                lexeme=self.source[self._start : self._current],
                line=self._line,
            )
        )

    def _match(self, char: str) -> bool:
        if self._at_end() or self.source[self._current] != char:
            return False
        self._current += 1
        return True

    def _peek(self) -> str:
        """looks ahead 1 character"""
        if self._at_end():
            return "\0"
        return self.source[self._current]

    def _peek_next(self) -> str:
        """looks ahead 2 character"""
        if self._current + 1 >= len(self.source):
            return "\0"
        return self.source[self._current + 1]

    def _advance(self) -> str:
        self._current += 1
        return self.source[self._current - 1]

    def _scan_token(self):
        charachter_list = list(self.source[self._start :])
        match charachter_list:
            case ["(", *_]:
                self._add(LEFT_PAREN)
                self._current += 1
            case [")", *_]:
                self._add(RIGHT_PAREN)
                self._current += 1
            case ["-", *_]:
                self._add(MINUS)
                self._current += 1
            case ["+", *_]:
                self._add(ADD)
                self._current += 1
            case ["*" | "×", *_]:
                self._add(TIMES)
                self._current += 1
            case ["/" | "÷", *_]:
                self._add(DIVIDE)
                self._current += 1
            case ["=", *_]:
                self._add(EQUAL)
                self._current += 1
            case ["≠", *_]:
                self._add(NOT_EQUAL)
                self._current += 1
            case ["≤", *_]:
                self._add(LESS_EQUAL)
                self._current += 1
            case ["≥", *_]:
                self._add(GREATER_EQUAL)
                self._current += 1
            case [":", *_]:
                self._add(COLON)
                self._current += 1
            case ["!", "=", *_]:
                self._add(NOT_EQUAL)
                self._current += 1
            case ["<", "-", *_]:
                self._add(ASSIGNMENT)
                self._current += 2
            case ["<", "=", *_]:
                self._add(LESS_EQUAL)
                self._current += 2
            case ["<", *_]:
                self._add(LESS)
                self._current += 1
            case [">", "=", *_]:
                self._add(GREATER_EQUAL)
                self._current += 2
            case [">", *_]:
                self._add(GREATER)
                self._current += 1

            case ["#", *_]:
                while self._peek() != "\n" and not self._at_end():
                    self._current += 1

            case ['"', *_]:
                self._current += 1
                while self._peek() != '"' and not self._at_end():
                    if self._peek() == "\n":
                        errors.error(self._line, "unterminated string")
                    self._current += 1

                if self._at_end():
                    errors.error(self._line, "unterminated string")

                # the closing `"`
                self._current += 1
                self._add(STRING, self.source[self._start + 1 : self._current - 1])

            case ["'", *_]:
                self._current += 1
                while self._peek() != "'" and not self._at_end():
                    if self._peek() == "\n":
                        errors.error(self._line, "unterminated string")
                    self._current += 1

                if self._at_end():
                    errors.error(self._line, "unterminated string")

                # the closing `'`
                self._current += 1
                self._add(STRING, self.source[self._start + 1 : self._current - 1])

            case ["\n", *_]:
                print("\n")
                self._current += 1
                self._line += 1
                return

            case [" ", *_] | ["\r", *_] | ["\t", *_]:
                self._current += 1
                return

            case [character, *_] if character.isdigit():
                # variable
                while self._peek().isdigit():
                    self._current += 1

                if self._peek() == "." and self._peek_next().isdigit():
                    # consume the '.'
                    self._current += 1

                    while self._peek().isdigit():
                        self._current += 1
                self._add(NUMBER, self.source[self._start : self._current])

            case [character, *_] if character.isalpha() or character == "_":
                while self._peek().isalpha() or self._peek() == "_":
                    self._current += 1

                text = self.source[self._start : self._current].lower()
                if text == "true":
                    self._add(TRUE)
                elif text == "false":
                    self._add(FALSE)
                elif text == "not":
                    self._add(NOT)
                elif text == "none":
                    self._add(NONE)
                elif text == "and":
                    self._add(AND)
                elif text == "or":
                    self._add(OR)
                elif text == "if":
                    self._add(IF)
                elif text == "then":
                    self._add(THEN)
                elif text == "end":
                    self._add(END)
                elif text == "endif":
                    self._add(END)
                elif text == "else":
                    self._add(ELSE)
                elif text == "while":
                    self._add(WHILE)
                elif text == "endwhile":
                    self._add(END)
                elif text == "for":
                    self._add(FOR)
                elif text == "to":
                    self._add(TO)
                elif text == "step":
                    self._add(STEP)
                elif text == "endfor":
                    self._add(END)
                elif text in {"print", "output"}:
                    self._add(PRINT)
                else:
                    self._add(IDENTIFIER)

            case _:
                errors.error(self._line, "Unexpected character")

    def scan_tokens(self) -> list[Token]:
        while self._current < len(self.source):
            self._start = self._current
            self._scan_token()
        return self._tokens + [Token(EOF, line=self._line)]

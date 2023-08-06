from AQAInterpreter.errors import *
from dataclasses import dataclass, field


@dataclass
class Environment:
    values: dict[str, object] = field(default_factory=dict)

    def get(self, name: Token) -> object:
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        raise AQARuntimeError(name, f"undefined variable '{name.lexeme}'")

    def define(self, name: str, value: object) -> None:
        self.values[name] = value
        
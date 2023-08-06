from AQAInterpreter.tokens import *
from AQAInterpreter.scanner import *
from AQAInterpreter.errors import *
from AQAInterpreter.environment import Environment
from abc import abstractmethod


environment = Environment()


class Expr:
    @abstractmethod
    def interpret(self) -> object:
        ...


class Stmt:
    @abstractmethod
    def interpret(self) -> object:
        ...


def paren(name: str, *exprs: Expr) -> str:
    string = "(" + name
    for expr in exprs:
        string += " "
        string += expr.dump()
    string += ")"

    return string


def check_number(operator: Token, *operands: object):
    try:
        [float(operand) for operand in operands]
    except Exception:
        raise AQARuntimeError(operator, "operand must be a number")


@dataclass
class Literal(Expr):
    value: object

    def interpret(self):
        return self.value


@dataclass
class Logical(Expr):
    left: Expr
    operator: Token
    right: Expr

    def interpret(self):
        left = self.left.interpret()
        right = self.right.interpret()

        if self.operator.type == OR:
            if left:
                return left
        else:
            # operator is AND
            if not left:
                return left

        return right


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def interpret(self):
        if (type := self.operator.type) == MINUS:
            return -self.right.interpret()
        elif type == NOT:
            return not self.right.interpret()


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def interpret(self):
        left = self.left.interpret()
        right = self.right.interpret()

        if (token_type := self.operator.type) == ADD:
            if (type(left), type(right)) in {(str, int), (int, str)}:
                return str(left) + str(right)
            else:
                return left + right
        elif token_type == MINUS:
            return left - right
        elif token_type == TIMES:
            return left * right
        elif token_type == DIVIDE:
            return left / right
        elif token_type == GREATER:
            return left > right
        elif token_type == GREATER_EQUAL:
            return left >= right
        elif token_type == LESS:
            return left < right
        elif token_type == LESS_EQUAL:
            return left <= right
        elif token_type == EQUAL:
            return left == right
        elif token_type == NOT_EQUAL:
            return left != right


@dataclass
class Grouping(Expr):
    expression: Expr

    def interpret(self):
        return self.expression.interpret()


@dataclass
class Variable(Expr):
    name: Token

    def interpret(self) -> object:
        return environment.get(self.name)


@dataclass
class Print(Stmt):
    expression: Expr

    def interpret(self):
        print(self.expression.interpret())


@dataclass
class While(Stmt):
    condition: Expr
    body: list[Stmt]

    def interpret(self) -> object:
        while self.condition.interpret():
            for stmt in self.body:
                stmt.interpret()


@dataclass
class If(Stmt):
    condition: Expr
    then_branch: list[Stmt]
    else_branch: list[Stmt]

    def interpret(self):
        if self.condition.interpret():
            for stmt in self.then_branch:
                stmt.interpret()

        else:
            for stmt in self.else_branch:
                stmt.interpret()


@dataclass
class Var(Stmt):
    name: Token
    initialiser: Expr

    def interpret(self):
        value = None
        if self.initialiser != None:
            value = self.initialiser.interpret()

        environment.define(self.name.lexeme, value)


if __name__ == "__main__":
    [
        Var(
            Token(type="IDENTIFIER", lexeme="i", line=1),
            initialiser=Literal(value=1),
        ),
        While(
            condition=Binary(
                left=Variable(name=Token(type="IDENTIFIER", lexeme="i", line=2)),
                operator=Token(type="LESS_EQUAL", lexeme="<=", line=2),
                right=Literal(value=5),
            ),
            body=[
                If(
                    condition=Binary(
                        left=Variable(
                            name=Token(type="IDENTIFIER", lexeme="i", line=3)
                        ),
                        operator=Token(type="EQUAL", lexeme="=", line=3),
                        right=Literal(value=3),
                    ),
                    then_branch=[
                        Print(expression=Literal(value="3 is a lucky number"))
                    ],
                    else_branch=[
                        Print(
                            expression=Variable(
                                name=Token(type="IDENTIFIER", lexeme="i", line=6)
                            )
                        )
                    ],
                ),
                Var(
                    name=Token(type="IDENTIFIER", lexeme="i", line=8),
                    initialiser=Binary(
                        left=Variable(
                            name=Token(type="IDENTIFIER", lexeme="i", line=8)
                        ),
                        operator=Token(type="ADD", lexeme="+", line=8),
                        right=Literal(value=1),
                    ),
                ),
            ],
        ),
    ]

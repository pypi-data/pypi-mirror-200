from AQAInterpreter.interpreter import *
from AQAInterpreter.tokens import *
from AQAInterpreter import errors


def parse(tokens: list[Token]):
    current = 0

    def error(token: Token, message: str):
        errors.error(token, message)
        had_error = True
        return AQAParseError(token, message)

    def match_token(*token_types: str) -> bool:
        for token_type in token_types:
            if check(token_type):
                advance()
                return True
        return False

    def consume(token_type: str, message: str) -> Token:
        if check(token_type):
            return advance()
        raise AQAParseError(peek(), message)

    def synchronize() -> None:
        advance()

        while not at_end():
            if previous().type == NEWLINE:
                return
            advance()


    def check(token_type: str) -> bool:
        if at_end():
            return False
        return peek().type == token_type

    def advance() -> Token:
        nonlocal current
        if not at_end():
            current += 1
        return previous()

    def at_end() -> bool:
        return peek().type == EOF

    def peek() -> Token:
        return tokens[current]

    def previous() -> Token:
        return tokens[current - 1]

    def primary() -> Expr:
        if match_token(FALSE):
            return Literal(False)
        elif match_token(TRUE):
            return Literal(True)
        elif match_token(NONE):
            return Literal(None)
        elif match_token(STRING):
            return Literal(previous().literal)
        elif match_token(NUMBER):
            if previous().literal.isdecimal():
                return Literal(int(previous().literal))
            else:
                return Literal(float(previous().literal))
        elif match_token(LEFT_PAREN):
            expr = expression()
            consume(RIGHT_PAREN, "Expected ')' after expression.")
            return Grouping(expr)
        elif match_token(IDENTIFIER):
            return Variable(previous())

        raise error(peek(), "Expect expression")

    def unary() -> Expr:
        if match_token(NOT, MINUS):
            operator = previous()
            right = unary()
            return Unary(operator, right)

        return primary()

    def factor():
        expr = unary()

        while match_token(DIVIDE, TIMES):
            expr = Binary(expr, previous(), factor())

        return expr

    def term():
        expr = factor()

        while match_token(MINUS, ADD):
            operator = previous()
            right = factor()
            expr = Binary(expr, operator, right)

        return expr

    def comparison():
        expr = term()

        while match_token(GREATER, GREATER_EQUAL, LESS, LESS_EQUAL):
            operator = previous()
            right = term()
            expr = Binary(expr, operator, right)

        return expr

    def equality():
        expr = comparison()

        while match_token(NOT_EQUAL, EQUAL):
            operator = previous()
            right = comparison()
            expr = Binary(expr, operator, right)

        return expr

    def and_():
        expr = equality()

        while match_token(AND):
            expr = Logical(expr, previous(), equality())

        return expr

    def or_():
        expr = and_()

        while match_token(OR):
            expr = Logical(expr, previous(), and_())

        return expr

    def expression():
        return or_()

    def print_statement():
        value = expression()
        return (Print(value),)

    def while_statement():
        condition = expression()
        statements = []

        if peek().type in {DO, COLON}:
            match_token(DO, COLON)

        while not match_token(END):
            if peek().type == EOF:
                raise error(peek(), "Expected END after WHILE loop")

            stmt = statement()
            if stmt is not None:
                statements.extend(stmt)

        return (While(condition, statements),)

    def for_statement():
        initialiser = var_declaration()[0]
        consume(TO, "Expect TO inside of FOR loop. ")
        stop = expression()
        statements = []

        # if start and stop are constant expressions interpreting them won't raise an undeclared variable error
        step = Literal(value=1)
        try:
            if (start_value := initialiser.initialiser.interpret()) == (
                stop_value := stop.interpret()
            ):
                condition = EQUAL
            elif start_value < stop_value:
                condition = LESS_EQUAL
            # set default step to -1 start_value > stop_value
            elif start_value > stop_value:
                condition = GREATER_EQUAL
                step = Literal(value=-1)

            if match_token(STEP):
                step = expression()
        except:
            consume(
                STEP,
                "step needs to be specified where start or stop are not constant expressions",
            )
            step = expression()
            condition = LESS_EQUAL if step.value > 0 else GREATER_EQUAL

        while not match_token(END):
            if peek().type == EOF:
                raise error(peek(), "Expected TO inside FOR loop")
            stmt = statement()
            if stmt is not None:
                statements += stmt

        out = initialiser, While(
            condition=Binary(
                left=Variable(name=initialiser.name),
                operator=Token(type=condition),
                right=stop,
            ),
            body=[stmt for stmt in statements]
            + [
                Var(
                    name=initialiser.name,
                    initialiser=Binary(
                        left=Variable(name=initialiser.name),
                        operator=Token(type=ADD),
                        right=step,
                    ),
                ),
            ],
        )
        return out

    def if_statement():
        condition = expression()
        then_branch, else_branch = [], []

        if peek().type in {THEN, COLON}:
            match_token(THEN, COLON)

        while not match_token(END):
            if peek().type == EOF:
                raise error(peek(), "Expected END after IF statement")

            stmt = statement()
            if stmt is not None:
                then_branch.extend(stmt)

            if match_token(ELSE):
                while not match_token(END):
                    if peek().type == EOF:
                        raise error(peek(), "Expected END after IF statement")
                    stmt = statement()
                    if stmt is not None:
                        else_branch.extend(stmt)
                break

        return (If(condition, then_branch, else_branch),)

    def statement_not_var():
        nonlocal current
        while True:
            if match_token(PRINT):
                return print_statement()
            elif match_token(WHILE):
                return while_statement()
            elif match_token(FOR):
                return for_statement()
            elif match_token(IF):
                return if_statement()
            elif tokens[current].type == EOF:
                return
            current += 1
            return

    def var_declaration():
        name = consume(IDENTIFIER, "Expect variable name. ")
        initialiser = expression() if match_token(ASSIGNMENT) else None
        # consume(NEWLINE, "Expect newline after variable deceleration")
        return (Var(name, initialiser),)

    def statement():
        try:
            for token in tokens[current :]:
                if token.type in {PRINT, WHILE, FOR, IF}:
                    return statement_not_var()
                elif token.type == ASSIGNMENT:
                    return var_declaration()
        except AQAParseError as e:
            errors.error(e.token, e.message)
            synchronize()
            return None

    def parse():
        statements: list[Stmt] = []
        while not at_end():
            stmt = statement()
            if stmt is not None:
                statements.extend(stmt)
        return statements

    return parse()

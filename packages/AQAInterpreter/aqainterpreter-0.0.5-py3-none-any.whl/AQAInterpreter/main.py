from AQAInterpreter.tokens import *
from AQAInterpreter.scanner import Scanner
from AQAInterpreter import parser
from pprint import pprint
import click

DEBUG = True


def run(source: str):
    had_error = False
    source += "\n"
    if DEBUG:
        print(source)
    tokens = Scanner(source).scan_tokens()
    # pprint(tokens)

    if DEBUG:
        pprint(tokens)
        print()
    statements = parser.parse(tokens)
    if statements is not None:
        if DEBUG:
            # pprint(statements)
            print(statements)
        for statement in statements:
            if statement is not None:
                statement.interpret()

    if had_error:
        exit(65)


@click.command()
@click.argument("filename", required=False)
@click.option("-c", "--cmd")
def main(filename, cmd):
    if filename and cmd:
        raise click.UsageError("cannot specify both filename and command")

    if filename:
        with open(filename, encoding="utf-8") as infp:
            cmd = infp.read()
    else:
        while True:
            run(input("> "))

    run(cmd)


if __name__ == "__main__":
    main()

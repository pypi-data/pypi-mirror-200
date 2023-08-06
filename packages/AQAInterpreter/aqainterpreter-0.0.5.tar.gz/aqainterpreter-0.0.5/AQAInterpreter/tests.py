""" Run these tests with
pytest AQAInterpreter/tests.py --verbose
"""

from contextlib import redirect_stdout
from AQAInterpreter import main
from io import StringIO


def run(*lines):
    code = "\n".join(list(lines))
    with redirect_stdout(io := StringIO()):
        main.run(code)
    return io.getvalue()


# Do not show tokens list or ast
main.DEBUG = False


def test_expressions():
    assert run("OUTPUT 1 + 1") == "2\n"
    assert run("OUTPUT 1 - 1") == "0\n"
    assert run("OUTPUT -1") == "-1\n"
    assert run("OUTPUT 2 * 1") == "2\n"
    assert run("OUTPUT 2 × 1") == "2\n"
    assert run("OUTPUT 2 / 1") == "2.0\n"
    assert run("OUTPUT 2 ÷ 1") == "2.0\n"

    assert run('OUTPUT "hi" + "÷"') == "hi÷\n"
    assert run('OUTPUT "a" * 3') == "aaa\n"

    assert run("OUTPUT 1 > 0") == "True\n"
    assert run("OUTPUT 1 ≥ 0") == "True\n"
    assert run("OUTPUT 1 >= 1") == "True\n"
    assert run("OUTPUT 1 < 0") == "False\n"
    assert run("OUTPUT 1 ≤ 0") == "False\n"
    assert run("OUTPUT 1 <= 1") == "True\n"


def test_comments():
    assert run("# comment") == ""


def test_assignment():
    assert run("a <- 0", "a <- a + 1", "OUTPUT a") == "1\n"


def test_if_statements():
    assert run('IF True OUTPUT "yes" ENDIF') == "yes\n"
    assert run('IF True OUTPUT "" OUTPUT "" ENDIF') == "\n\n"
    assert run('IF False OUTPUT "yes" ENDIF') == ""
    assert run('IF False OUTPUT "yes" ELSE OUTPUT "no" ENDIF') == "no\n"
    assert run('IF True IF True OUTPUT "yes" ENDIF ENDIF') == "yes\n"


def test_while_loops():
    assert run("a <- 1", "while a <= 3 DO", "output a", "a <- a + 1", "endwhile") == "1\n2\n3\n"
    
    # fibonacci sequence
    assert (
        run(
            "a <- 1",
            "b <- 1",
            "c <- 2",
            "count <- 0",
            "WHILE count != 2",
            "    OUTPUT a",
            "    a <- b + c",
            "    OUTPUT b",
            "    b <- c + a",
            "    OUTPUT c",
            "    c <- a + b",
            "    count <- count + 1",
            "ENDWHILE",
        )
        == "1\n1\n2\n3\n5\n8\n"
    )


def test_for_loops():
    assert (
        run("FOR a <- 1 TO 1", "OUTPUT a", "ENDFOR")
        == run("FOR a <- 1 TO 1 STEP 1", "OUTPUT a", "ENDFOR")
        == run("FOR a <- 1 TO 1 STEP -1", "OUTPUT a", "ENDFOR")
        == "1\n"
    )
    assert (
        run("FOR a <- 1 TO 3", "OUTPUT a", "ENDFOR")
        == run("FOR a <- 1 TO 3 STEP 1", "OUTPUT a", "ENDFOR")
        == "1\n2\n3\n"
    )

    assert (
        run("FOR a <- 3 TO 1", "OUTPUT a", "ENDFOR")
        == run("FOR a <- 3 TO 1 STEP -1", "OUTPUT a", "ENDFOR")
        == "3\n2\n1\n"
    )

    assert run("FOR a <- 1 TO 5 STEP 2", "OUTPUT a", "ENDFOR") == "1\n3\n5\n"
    assert run("FOR a <- 5 TO 1 STEP -2", "OUTPUT a", "ENDFOR") == "5\n3\n1\n"

    # nested for loop
    assert (
        run(
            "FOR a <- 1 TO 2",
            "   FOR b <- 1 TO 2",
            "       OUTPUT a",
            "       OUTPUT b",
            "       OUTPUT ''",
            "   ENDFOR",
            "ENDFOR",
        )
        == "1\n1\n\n1\n2\n\n2\n1\n\n2\n2\n\n"
    )


# FOR a <- 1 TO 12
#     FOR b <- 1 TO 12
#         OUTPUT a + " × " + b + " = " + (a * b)
#     END
# END



# for i <- 1 to 5
#     num <- 1
#     for j <- 1 to (i)
#         num <- num * -1
#     endfor
#     output i * num
# endfor
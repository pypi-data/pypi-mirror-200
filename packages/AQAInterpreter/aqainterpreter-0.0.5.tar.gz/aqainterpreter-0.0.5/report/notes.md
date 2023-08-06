Lox is a scripting language with curly braces, similar to js. The book takes you though writing a tree-walk implementation in js and a byte-code implementation in c.


## Tree walk interpreter

1. scanning / tokenizing
    
    ```julia
    "output 5 + 31" -> ["output", "5", "+", "31"]
    ```
    
    each element in the above list, is known as a lexeme

2. parsing 
    
    
    ```julia
    ["output", "5", "+", "31"] ->

    output  # statement
      |
      +   # binary operation
     / \
    5   31  # constants
    ```

3. Traverse tree and evaluate it 

4. Or traverse tree and transpile it to ruby
- Compiler compilers are programs which take in grammar and create an interpreter for said grammar. For example yacc and Lex

- Languages can be dynamically typed of statically typed meaning type checking is done at runtime or compile time, lox is dynamically typed



Most language grammars use a flavour of bnf
a 'string' is made up of the 'alphabet'


| program        | Lexical grammar | Syntactic grammar |
| -------------- | --------------- | ----------------- |
| alphabet       | characters      | tokens            |
| string         | tokens          | expressions       |
| implemented by | scanner         | parser            |

a production has a head and body
the head is the name
the body is the actual rule
the body can be terminal or non-terminal

A terminal production is part of the alphabet
a non-terminal rule can link to another rule

For example: 

```julia
# BNF style grammar

# non-terminal rules
sentence ->  "There are " + num + " " + "animals at the " +  place

num ->  num + digit
num ->  digit

# terminal rules
digit  ->  1
digit  ->  2
digit  ->  3
...
digit  ->  9

place ->  "Farm"
place ->  "Zoo"

# e.g. `There are 3 animals at the zoo
```


python asts can be printed via
```python
from ast import dump, parse
print(dump(parse('1 + 1'), indent=4))
```



I want the traceback to either use python technology
implement my own. I want if the user has a function 
to support a full traceback of their program
but an optional flag that will make it so the full traceback
of interpreter.py is shown instead 

For now lets show the full traceback which we don't mind seing
and well check this issue out later when we go about implementing
functions. 

Currently skipped
- assignment syntax returning a value so `a <- b <- 1` doesn't work. p122 8.4
- expression blocks p125 8.5
- expression statements working in the REPL

The bnf the book uses is
```ruby
forStmt  ->  "for" "(" ( varDecl | exprStmt | ";" ) expression? ";" expression? ")" statement ;
```

actually for arrays we probably want a `len` function so maybe we should do functions first. Or should I finish for loops for the sake of completion.

ok for the billionth time here is bnf for a for loop
```ruby
forStmt  ->  "for" varDecl "to" expression ("step" expression)? list[stmt] 
```
ok we have a problem where the varDecl does a lookahead but that will brick in a for loop
so in the statement() function we lookahead to end of line before a FOR or NEWLINE
ok what is the actual parser code for a `for_statement`


## BNF

expressions
```ruby
program     -> declaration* EOF

declaration -> varDecl | stmt

stmt        -> printStmt
            | ifStmt
            | whileStmt
            | forStmt

varDecl     -> IDENTIFIER "<-" expression

printStmt   -> ( "PRINT" | "OUTPUT" ) expression

ifStmt      -> "IF" expression ( "THEN" | ":" )? decleration* ( "ELSE" decleration* )? "ENDIF"

whileStmt   -> "WHILE" expression ( "DO" | ":" ) decleration* "ENDWWHILE"

forStmt     ->  "FOR" varDecl "TO" expression ( "STEP" expression )? decleration*

expression  -> assignment
logic_or    -> logic_and ( "or" logic_and )*
logic_and   -> equality ( "and" equality )*
equality    -> comparison ( ( "!=" | "==" ) comparison )*
comparison  -> term ( ( ">" | ">=" | "<" | "<=" ) term )*
term        -> factor ( ( "-" | "+" ) factor )*
factor      -> unary ( ( "/" | "*" ) unary )*
unary       ->  ( "!" | "-" ) unary |  primary
primary     ->  INTEGER | REAL | STRING | "True" | "False" |
                "None" | "(" expression ")"
```




\pagebreak

```aqa
i <- 1
WHILE i <= 5
    IF i = 3
        OUTPUT "3 is a lucky number"
    ELSE
        PRINT(i)
    END
    i <- i + 1
END
```
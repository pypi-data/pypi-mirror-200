from dataclasses import dataclass, field

@dataclass
class Token:
    type: str
    literal: str | None = field(repr=False, default=None)
    lexeme: str = ""
    line: int = 0


# single character tokens
LEFT_PAREN = "LEFT_PAREN"
RIGHT_PAREN = "RIGHT_PAREN"
COLON = "COLON"
ADD = "ADD"
MINUS = "MINUS"
TIMES = "TIMES"
DIVIDE = "DIVIDE"
NEWLINE = "NEWLINE"

# Single or double character tokens
NOT = "NOT"
NOT_EQUAL = "NOT_EQUAL"
EQUAL = "EQUAL"
ASSIGNMENT = "ASSIGNMENT" 
GREATER = "GREATER"
GREATER_EQUAL = "GREATER_EQUAL"
LESS = "LESS"
LESS_EQUAL = "LESS_EQUAL" 

# Literals
IDENTIFIER = "IDENTIFIER"
STRING = "STRING"
NUMBER = "NUMBER" 

# Keywords
TRUE = "TRUE"
FALSE = "FALSE"
NONE = "NONE"
AND = "AND"
OR = "OR"
IF = "IF"
THEN = "THEN"
ELSE = "ELSE" 
WHILE = "WHILE"
DO = "DO"
END = "END"
FOR = "FOR"
TO = "TO" 
STEP = "STEP"
PRINT = "PRINT"

# End of file token
EOF = "EOF"

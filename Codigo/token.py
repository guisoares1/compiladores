from dataclasses import dataclass
from enum import Enum, auto

class TokenEnum(Enum):
    NONE = -1
    FUNCTION = 'FUNCTION'
    ACHA = '{' 
    FCHA = '}'
    DPONTOS = ':'
    CHAR = 'CHAR'
    INT = 'INT'
    FLOAT = 'FLOAT'
    ID = 'ID'
    VIRGULA = ','
    PVIRGULA = ';'
    SE = 'SE' 
    SENAO = 'SENAO'
    APAR = '('
    FPAR = ')' 
    ENQUANTO = 'ENQUANTO'
    FACA = 'FACA'
    RELOP = 'RELOP'
    LE = '<='
    LT = '<'
    GE = '>='
    GT = '>'
    EQ = '=='
    NE = '<>'
    SUM = '+'
    DIF = '-'
    MULT = '*'
    DIV = '/'
    EXP = '^'
    ATRIB = '='
    CONINT = 'CONSINT'
    INUM = auto()
    PFNUM = auto() # ponto fixo (PF) 
    NCNUM = auto() # notação científica (NC)
    ATE = auto() 
    CONCHAR = 'CONSCHAR'
    EOF = auto() # end of file $
    ENTAO = "ENTAO"
    REPITA = "REPITA"

    # tipos já existentes antes
    PROGRAMA = auto()
    BEGIN = auto()
    END = auto()
    TYPE = auto()
    NUM = auto()
    FNUM = auto()
    LITERAL = auto()
    ATTR = auto() # := 
    IF = auto()
    THEN = auto()
    ELSE = auto()
    REPEAT = auto()
    WHILE = auto()
    DO = auto()
    LPAR = auto() # LPAR (
    RPAR = auto() # RPAR )
    DD = auto() # double dot :
    CD = auto() # comma dot ;
    COMMA = auto() # comma ,

@dataclass(init=True)
class Token: # trocar nome atributos
    """Tokens serão representados na forma <Token.name, Token.Attribute>"""
    name: int
    attribute: int
    line: int
    col: int

    def __repr__(self) -> str:
        return f'Token <{Token(self.name).name}, {Token(self.attribute).name}> l:{self.line} c:{self.col}'


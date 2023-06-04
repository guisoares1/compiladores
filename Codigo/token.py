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
    CONINT = 'CONSTINT'
    INUM = auto()
    PFNUM = auto() # ponto fixo (PF) 
    NCNUM = auto() # notação científica (NC)
    CONSTFLOAT = 'CONSTFLOAT'
    ATE = 'ATE' 
    CONCHAR = 'CONSTCHAR'
    EOF = '$' # end of file $
    ENTAO = "ENTAO"
    REPITA = "REPITA"

@dataclass(init=True)
class Token:
    nome: TokenEnum
    atributo: str
    linha: int
    coluna: int



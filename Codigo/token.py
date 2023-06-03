from dataclasses import dataclass
from enum import Enum, auto

class TokenEnum(Enum):
    NONE = -1
    FUNCTION = auto()
    ACHA = auto() # {
    FCHA = auto() # }
    DPONTOS = auto() # :
    CHAR = auto()
    INT = auto()
    FLOAT = auto()
    ID = auto()
    VIRGULA = auto() # ,
    PVIRGULA = auto() # ;
    SE = auto() 
    SENAO = auto()
    APAR = auto() # (
    FPAR = auto() # ) 
    ENQUANTO = auto()
    FACA = auto()
    RELOP = auto()
    LE = auto() # <=
    LT = auto() # <
    GE = auto() # >=
    GT = auto() # >
    EQ = auto() # ==
    NE = auto() # <>
    SUM = auto()
    DIF = auto()
    MULT = auto()
    DIV = auto()
    EXP = auto()
    ATRIB = auto() # = 
    INUM = auto()
    PFNUM = auto() # ponto fixo (PF) 
    NCNUM = auto() # notação científica (NC)
    ATE = auto() 
    CONCHAR = auto() # constante char
    EOF = auto() # end of file $
    ENTAO = auto()
    REPITA = auto()

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
    lexema: str

    def __repr__(self) -> str:
        return f'Token <{Token(self.name).name}, {Token(self.attribute).name}> l:{self.line} c:{self.col}'


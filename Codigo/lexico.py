from Codigo.TabelaSimbolos import TabelaSimbolos
from SymbolTable import *
from Token import *

class Analyzer:
  source_file:str
  source_code = None

  def __init__(self, path:str) -> None:
    self.source_file = path
    self.source_code = open(self.source_file, "rb")
    print("[lexical] Iniciando analisador lexico")
    print("[lexical] Arquivo fonte aberto")
    self.begin()

  #loop do analisador
  def begin(self):
    self.digitos = [str(x) for x in range(10)] # [0-9]
    self.letra_ = [chr(x) for x in range(65, 91)] # [A-Z]
    self.letra_ += [chr(x) for x in range(97, 123)] # [a-z]
    self.letra_ += '_'
    print("[lexical] Vetores auxiliares criados")

  def stop(self):
    self.source_code.close()
    print("[lexical] Arquivo fonte fechado")

  def lex(self):
    state = 0
    w = ""
    line = 0
    col = 0
    lookahead = False #flag pra identificar se fez lookahead ou não
   
    st = TabelaSimbolos()
    while(True):
        
        s = str(state)
        if not s.startswith('t'): 
          try:
            c = self.source_code.read(1) #se não fez lookahead, e não está em um estado final, lê next char
            c = c.decode('UTF-8')
            if not c in ['\t', '\r', '\n', ' ', ',']:
              w += c 
              #print(f"[lexical] Estado: {state} simbolo: {c} lexema: {w}")
          except StopIteration:
            print("Fim do arquivo, “cadeia rejeitada")
            break

        
        if c == '\n':
          line += 1
          col = 0

        col += 1

        match s:
          case '0': #estado 0 inicial
            if c == '<':
              state = 60
            elif c == '>':
              state = 61
            elif c == '=':
              state = 13
            elif c in self.digitos: # digitos
              state = 54 # numero diagrama 
            elif c == 'f':
              state = 5
            elif c == 'i':
              state = 6
            elif c == 'c':
              state = 7
            elif c == 's':
              state = 8
            elif c == 'r':
              state = 9
            elif c == 'a':
              state = 10
            elif c in self.letra_: # letras diferentes das iniciais (tokens)
              state = 12
            elif c == '(':
              state = 't1'
            elif c == ')':
              state = 't2'
            elif c == '+':
              state = 't3'
            elif c == '-':
              state = 't4'
            elif c == '*':
              state = 't5'
            elif c == '/': # tratar se é comentario ou divisao
              state = 17
            elif c == '^':
              state = 't6'
            elif c in ['\t', '\n', ' ']: # pulo de linha
              state = 14
            elif c == ';':
              state = 't7'
            elif c == ',':
              state = 't8'
            elif c == '\'':
              state = 62
            elif c == '$': # fim arquivo
              state = 't9'

          ########################### RELOP ###########################
          case '60':
            if c == '=': 
              state = 't10' # <=
            elif c == '>': 
              state = 't11' #  <> 
            else :
              state = 't12' # < lookahead
          
          case '61':
            if c == '=': 
              state = 't13' # >=
            else: 
              state = 't14' # > lookahead
          
          case '13':
            if c == '=': 
              state = 't15' # == 
            else:
              state = 't16' # =  lookahead

          case 't10':
            state = 0
            token = Token(token.RELOP, token.LE, line, col)
            print(f"lex - Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.RELOP 
          
          case 't11':
            state = 0
            token = Token(token.RELOP, token.NE, line, col)
            print(f"lex - Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.RELOP 
          
          case 't12':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            token = Token(token.RELOP, token.LT, line, col)
            print(f"lex - Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.RELOP
          
          case 't13':
            state = 0
            token = Token(token.RELOP, token.GE, line, col)
            print(f"lex - Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.RELOP 
          
          case 't14':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            token = Token(token.RELOP, token.GT, line, col)
            print(f"lex - Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.RELOP
          
          case 't15':
            state = 0
            token = Token(token.RELOP, token.EQ, line, col)
            print(f"lex - Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.RELOP
          
          case 't16':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            token = Token(token.ATRIB, token.NONE, line, col)
            print(f"lex - Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.ATRIB
          
          ###################### Monotoken ########################
          case 't1':
            state = 0
            token = Token(token.APAR, token.NONE, line, col)
            print(f"lex - Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.APAR 
          
          case 't2':
            state = 0
            token = Token(token.FPAR, token.NONE, line, col)
            print(f"lex - Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.FPAR 
          
          case 't3':
            state = 0
            token = Token(token.SUM, token.NONE, line, col)
            print(f"lex - Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.SUM
          
          case 't4':
            state = 0
            token = Token(token.DIF, token.NONE, line, col)
            print(f"lex - Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.DIF
          
          case 't5':
            state = 0
            token = Token(token.MULT, token.NONE, line, col)
            print(f"lex - Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.MULT
          
          case 't6':
            state = 0
            token = Token(token.EXP, token.NONE, line, col)
            print(f"lex - Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.EXP
          
          case 't7':
            state = 0
            token = Token(token.PVIRGULA, token.NONE, line, col)
            print(f"lex - Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.PVIRGULA
          
          case 't8':
            state = 0
            token = Token(token.VIRGULA, token.NONE, line, col)
            print(f"lex - Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.VIRGULA
          
          case't22':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            token = Token(token.DIV, token.NONE, line, col)
            print(f"[lexical] Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.DIV 
        
          case 't9':
            print("lex - Fim do arquivo")
            return token.EOF
          ##################### NUMERO #####################
          case '54':
            if c in self.digitos:
              state = 54
            elif c == '.':
              state = 55
            else:
              state = 't17' # contInt lookahead

          case '55':
            if c in self.digitos:
              state = 56
            else:
              print(f'Error: é esperado um número e foi encontrado "{c}" l:{line} c:{col}')
              break

          case '56':
            if c in self.digitos:
              state = 56
            elif c == 'E':
              state = 58  
            else:
              state = 't18'   # PF lookahead

          case '58':
            if c in ['+', '-']:
              state = 57
            elif c in self.digitos:
              state = 59 
            else:
              print(f'Error: é esperado um número ou um [+ -] e foi encontrado "{c}" l:{line} c:{col}')  
              break
          case '59':
            if c in self.digitos:
              state = 59
            else :
              state = 't19'   # NC lookahead  

          case 't17':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            token = Token(token.INUM, token.NONE, line, col, )
            st.insert(token)
            print(f"[lexical] Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.INUM 
          
          case 't18':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            token = Token(token.PFNUM, token.NONE, line, col)
            st.insert(token)
            print(f"[lexical] Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.PFNUM 
          
          case 't19':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            token = Token(token.NCNUM, token.NONE, line, col)
            st.insert(token)
            print(f"[lexical] Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.NCNUM 
          
          #################### ConstChar ####################
          case '62':
            if c =='\'':
              state = "t20"

          case 't20':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            token = Token(token.CONCHAR, token.NONE, line, col)
            print(f"[lexical] Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.CONCHAR 
          
          ################### comentario ###################
          case '17':
            if c =='*':
              state = 15
            else:
              state = 't22'

          case '15':
            if c =='*':
              state = 16

          case '16':
            if c !='/':
              state = 15
            else:
              state = 't23'  

          case 't23':
            state = 0

          ################### tab ###################
          case '14':
            if c in ['\n', '\t', '\r', ' ']:
              state = 14
            else:
              state = 't21'

          case 't21':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)

          ################### ID ###################
          case '12':
            if c in self.digitos or c in self.letra_:
              state = 12
            else:
              state = 't24' # ID lookahead

          case 't24':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            w = w[:-1]
            token = Token(token.ID, token.NONE, line, col)
            print(f"[lexical] Token {token.name}, {token.attribute}, w: {w.strip()}")
            st.insert(token)
            return token.ID
          
          ################### Function ###################
          case '5':
            if c not in (self.digitos or c in self.letra_):
              state = 't24'  # ID lookahead 
            elif c == 'u':
              state = 18   # fu
            elif c == 'l':
              state = 19   # fl
            elif c == 'a':
              state = 20   # fa
            else:
              state = '12'  # outros

          case '18':
            if c == 'n':    # fun
              state = 21
            elif c not in (self.digitos or c in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '21': 
            if c == 'c':    # func
              state = 22
            elif c not in (self.digitos or c in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros

          case '22':
            if c == 't':    # funct
              state = 23
            elif c not in (self.digitos or c in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros

          case '23':
            if c == 'i':    # functi
              state = 24
            elif c not in (self.digitos or c in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '24':
            if c == 'o':    # functio 
              state = 25
            elif c not in (self.digitos or c in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '25':
            if c == 'n':    # function
              state = 26
            elif c not in (self.digitos or c in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '26':
            if c not in (self.digitos or c in self.letra_):
              state = 't25'
            else:
              state = '12'  # outros

          case 't25':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            w = w[:-1]
            token = Token(token.FUNCTION, token.NONE, line, col)
            print(f"[lexical] Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.FUNCTION

          ################### Float ###################
          
          case '19':
            if c == 'o':   # flo
              state = 27
            elif c not in (self.digitos or c in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '27':
            if c == 'a':   # floa
              state = 28
            elif c not in (self.digitos or c in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros

          case '28':
            if c == 't':   # float
              state = 29
            elif c not in (self.digitos or c in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros

          case '29':
            if c == 't':   # float
              state = 30
            elif c not in (self.digitos or c in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '30':
            if c not in (self.digitos or c in self.letra_):
              state = 't26'
            else:
              state = '12'  # outros

          case 't26':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            w = w[:-1]
            token = Token(token.FLOAT, token.NONE, line, col)
            print(f"[lexical] Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.FLOAT
          
          ################### faca ###################
          case '20':
            if c == 'c':   # fac
              state = 31
            elif c not in (self.digitos or c in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '31':
            if c == 'a':   # faca
              state = 32
            elif c not in (self.digitos or c in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros

          case '32':
            if c not in (self.digitos or c in self.letra_):
              state = 't27'
            else:
              state = '12'  # outros
            

          case 't27':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            w = w[:-1]
            token = Token(token.FACA, token.NONE, line, col)
            print(f"[lexical] Token {token.name}, {token.attribute}, w: {w.strip()}")
            return token.FACA
          
          ################### int ###################
          case '19':
            if c == 'o':   # flo
              state = 27
            elif c not in (self.digitos or c in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros



          

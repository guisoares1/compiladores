from TabelaSimbolos import TabelaSimbolos
from Token import *
import io

class Analyzer:
  source_file:str
  source_code = None

  def __init__(self, path:str) -> None:
    self.source_file = path
    self.source_code = open(self.source_file, "rb")
    print(path)
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
    lexema = ""
    line = 1
    col = 0
    lookahead = False #flag pra identificar se fez lookahead ou não
   
    st = TabelaSimbolos() 
    while(True):
        
        s = str(state)
        if not s.startswith('t'): 
          try:
            c = self.source_code.read(1) #se não fez lookahead, e não está em um estado final, lê next char
            print(c)
            c = c.decode('UTF-8') # resolver problema utf
            if not c in ['\t', '\r', '\n', ' ', ',']:
              lexema += c 
          except StopIteration:
            print("Fim do arquivo, “cadeia rejeitada")
            break

        if c in ['\\t', '\\n','\\r']:
          line += 1
          col = 1

        if line>100:
          break
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
              state = 72
            elif c == 'c':
              state = 7
            elif c == 's':
              state = 8
            elif c == 'r':
              state = 9
            elif c == 'a':
              state = 10
            elif c == 'e':
              state = 43
            elif c in self.letra_: # letras diferentes das iniciais (tokens)
              state = 12
            elif c == '(':
              state = 't1'
            elif c == ')':
              state = 't2'
            elif c == '{':
              state = 't36'
            elif c == '}':
              state = 't37'  
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
            elif c in ['\\t', '\\n', '\\r']: # pulo de linha
              state = 14
            elif c == ';':
              state = 't7'
            elif c == ',':
              state = 't8'
            elif c == ':':
              state = 't38'
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
            token = Token(TokenEnum.RELOP, TokenEnum.LE, line, col)
            print(f"lex - Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          
          case 't11':
            state = 0
            token = Token(TokenEnum.RELOP, TokenEnum.NE, line, col)
            print(f"lex - Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token 
          
          case 't12':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            token = Token(TokenEnum.RELOP, TokenEnum.LT, line, col)
            print(f"lex - Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          
          case 't13':
            state = 0
            token = Token(TokenEnum.RELOP, TokenEnum.GE, line, col)
            print(f"lex - Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          
          case 't14':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            token = Token(TokenEnum.RELOP, TokenEnum.GT, line, col)
            print(f"lex - Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          
          case 't15':
            state = 0
            token = Token(TokenEnum.RELOP, TokenEnum.EQ, line, col)
            print(f"lex - Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          
          case 't16':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            token = Token(TokenEnum.ATRIB, TokenEnum.NONE, line, col)
            print(f"lex - Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          
          ###################### Monotoken ########################
          case 't1':
            state = 0
            token = Token(TokenEnum.APAR, TokenEnum.NONE, line, col)
            print(f"lex - Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token 
          
          case 't2':
            state = 0
            token = Token(TokenEnum.FPAR, TokenEnum.NONE, line, col)
            print(f"lex - Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          
          case 't3':
            state = 0
            token = Token(TokenEnum.SUM, TokenEnum.NONE, line, col)
            print(f"lex - Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          
          case 't4':
            state = 0
            token = Token(TokenEnum.DIF, TokenEnum.NONE, line, col)
            print(f"lex - Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          
          case 't5':
            state = 0
            token = Token(TokenEnum.MULT, TokenEnum.NONE, line, col)
            print(f"lex - Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          
          case 't6':
            state = 0
            token = Token(TokenEnum.EXP, TokenEnum.NONE, line, col)
            print(f"lex - Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          
          case 't7':
            state = 0
            token = Token(TokenEnum.PVIRGULA, TokenEnum.NONE, line, col)
            print(f"lex - Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          
          case 't8':
            state = 0
            token = Token(TokenEnum.VIRGULA, TokenEnum.NONE, line, col)
            print(f"lex - Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          
          case 't36':
            state = 0
            token = Token(TokenEnum.ACHA, TokenEnum.NONE, line, col)
            print(f"lex - Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          
          case 't37':
            state = 0
            token = Token(TokenEnum.FCHA, TokenEnum.NONE, line, col)
            print(f"lex - Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          
          case't22':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            token = Token(TokenEnum.DIV, TokenEnum.NONE, line, col)
            print(f"[lexical] Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
        
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
            lexema = lexema[:-1]
            token = Token(TokenEnum.CONINT, TokenEnum.INUM, line, col, )
            st.insert(token)
            print(f"[lexical] Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token 
          
          case 't18':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            lexema = lexema[:-1]
            token = Token(TokenEnum.CONSTFLOAT, TokenEnum.PFNUM, line, col)
            st.insert(token)
            print(f"[lexical] Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          
          case 't19':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            lexema = lexema[:-1]
            token = Token(TokenEnum.CONSTFLOAT, TokenEnum.NCNUM, line, col)
            st.insert(token)
            print(f"[lexical] Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token 
          
          #################### ConstChar ####################
          case '62':
            if c =='\'':
              state = "t20"

          case 't20':
            state = 0
            lookahead = True
            token = Token(TokenEnum.CONCHAR, lexema, line, col)
            st.insert(token)
            print(f"[lexical] Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token 
          
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
            lexema = ""
            state = 0

          ################### tab ###################
          case '14':
            if c in ['\n', '\t', '\r']:
              state = 14
            else:
              state = 't21'

          case 't21':
            lookahead = True
            self.source_code.seek(-1, 1)
            lexema = lexema[:-1]
            state = 0


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
            lexema = lexema[:-1]
            token = Token(TokenEnum.ID, lexema, line, col)
            print(f"[lexical] Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            st.insert(token)
            return token
          
          ################### Function ###################
          case '5':
            if (c not in self.digitos) and (c not in self.letra_):
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
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '21': 
            if c == 'c':    # func
              state = 22
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros

          case '22':
            if c == 't':    # funct
              state = 23
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros

          case '23':
            if c == 'i':    # functi
              state = 24
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '24':
            if c == 'o':    # functio 
              state = 25
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '25':
            if c == 'n':    # function
              state = 26
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '26':
            if (c not in self.digitos) and (c not in self.letra_):
              state = 't25'
            else:
              state = '12'  # outros

          case 't25':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            lexema = lexema[:-1]
            token = Token(TokenEnum.FUNCTION, TokenEnum.NONE, line, col)
            print(f"[lexical] Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token

          ################### Float ###################
          
          case '19':
            if c == 'o':   # flo
              state = 27
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '27':
            if c == 'a':   # floa
              state = 28
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros

          case '28':
            if c == 't':   # float
              state = 29
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros

          case '29':
            if c == 't':   # float
              state = 30
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '30':
            if (c not in self.digitos) and (c not in self.letra_):
              state = 't26'
            else:
              state = '12'  # outros

          case 't26':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            lexema = lexema[:-1]
            token = Token(TokenEnum.FLOAT, TokenEnum.NONE, line, col)
            print(f"[lexical] Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          
          ################### faca ###################
          case '20':
            if c == 'c':   # fac
              state = 31
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '31':
            if c == 'a':   # faca
              state = 32
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros

          case '32':
            if (c not in self.digitos) and (c not in self.letra_):
              state = 't27'
            else:
              state = '12'  # outros
            

          case 't27':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            lexema = lexema[:-1]
            token = Token(TokenEnum.FACA, TokenEnum.NONE, line, col)
            print(f"[lexical] Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          
          ################### int ###################
          case '72':
            if c == 'n':   # in
              state = 33
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '33':
            if c == 't':   # int
              state = 34
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros

          case '34':
            if (c not in self.digitos) and (c not in self.letra_):
              state = 't28'
            else:
              state = '12'  # outros
          
          case 't28':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            lexema = lexema[:-1]
            token = Token(TokenEnum.INT, lexema, line, col)
            print(f"[lexical] Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          
          ################### char ###################
          case '7':
            if c == 'h':   # ch
              state = 35
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros

          case '35':
            if c == 'a':   # cha
              state = 36
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros

          case '36':
            if c == 'r':   # char
              state = 37
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '37':
            if (c not in self.digitos) and (c not in self.letra_):
              state = 't29'
            else:
              state = '12'  # outros

          case 't29':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            lexema = lexema[:-1] 
            token = Token(TokenEnum.CHAR, TokenEnum.NONE, line, col)
            print(f"[lexical] Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
        
          ################### senao ###################
          case '8':
            if c == 'e':   # se
              state = 38
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros

          case '38':
            if c == 'n':   # sen
              state = 39
            elif (c not in self.digitos) and (c not in self.letra_):
              state = 't31'
            else:
              state = '12'  # outros

          case '39':
            if c == 'a':   # sena
              state = 41
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '41':
            if c == 'o':   # senao
              state = 42
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '42':
            if (c not in self.digitos) and (c not in self.letra_):
              state = 't30'
            else:
              state = '12'  # outros

          case 't30':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            lexema = lexema[:-1] 
            token = Token(TokenEnum.SENAO, TokenEnum.NONE, line, col)
            print(f"[lexical] Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
        
          ################### se ###################
          case 't31':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            lexema = lexema[:-1] 
            token = Token(TokenEnum.SE, TokenEnum.NONE, line, col)
            print(f"[lexical] Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return TokenEnum.SE
          
          ################### entao ###################
          case '43':
            if c == 'n':   # en
              state = 44
            elif c == 'q':   # en
              state = 48
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '44':
            if c == 't':   # ent
              state = 45
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '45':
            if c == 'a':   # enta
              state = 46
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '46':
            if c == 'o':   # entao
              state = 47
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '47':
            if (c not in self.digitos) and (c not in self.letra_):
                state = 't32'
            else:
                state = '12'  # outros
          
          case 't32':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            lexema = lexema[:-1] 
            token = Token(TokenEnum.ENTAO, TokenEnum.ENTAO, line, col)
            print(f"[lexical] Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token

          ################### enquanto ###################

          case '48':
            if c == 'q':   # enq
              state = 49
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '49':
            if c == 'u':   # enqu
              state = 50
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros

          case '50':
            if c == 'a':   # enqua
              state = 51
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '51':
            if c == 'n':   # enquan
              state = 52
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '52':
            if c == 't':   # enquant
              state = 53
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '53':
            if c == 'o':   # enquanto
              state = 67
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '67':
            if (c not in self.digitos) and (c not in self.letra_):
                state = 't33'
            else:
                state = '12'  # outros
          
          case 't33':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            lexema = lexema[:-1] 
            token = Token(TokenEnum.ENQUANTO, TokenEnum.ENQUANTO, line, col)
            print(f"[lexical] Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          
          ################### repita ###################
          case '9':
            if c == 'e':   # re
              state = 68
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '68':
            if c == 'p':   # rep
              state = 69
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '69':
            if c == 'i':   # repi
              state = 57
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '57':
            if c == 't':   # repit
              state = 70
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros

          case '70':
            if c == 'a':   # repita
              state = 77
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '77':
            if (c not in self.digitos) and (c not in self.letra_):
                state = 't34'
            else:
                state = '12'  # outros
          
          case 't34':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            lexema = lexema[:-1] 
            token = Token(TokenEnum.REPITA, TokenEnum.REPITA, line, col)
            print(f"[lexical] Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token

          ################### ate ###################
          case '10':
            if c == 't':   # at
              state = 71
            elif (c not in self.digitos) and (c not in self.letra_): 
              state = 't24'   # ID lookahead 
            else:
              state = '12'  # outros
          
          case '71':
            if c == 'e':   # ate
              state = 66
          
          case '66':
            if (c not in self.digitos) and (c not in self.letra_):
                state = 't35'
            else:
                state = '12'  # outros
            
          case 't35':
            state = 0
            lookahead = True
            self.source_code.seek(-1, 1)
            lexema = lexema[:-1] 
            token = Token(TokenEnum.ATE, TokenEnum.ATE, line, col)
            print(f"[lexical] Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          
          case 't38':
            state = 0
            lookahead = True
            token = Token(TokenEnum.DPONTOS, TokenEnum.ATE, line, col)
            print(f"[lexical] Token {token.nome}, {token.atributo}, w: {lexema.strip()}")
            return token
          ###################
          case 't9':
            token = Token(TokenEnum.EOF, TokenEnum.ATE, line, col)
            print("lex - Fim do arquivo")
            return token




          











          

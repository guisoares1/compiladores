from cgitb import lookup
from dataclasses import dataclass, field
from typing import List, Union
from Token import *

@dataclass(init=True)
class Symbol:
  name:str
  attribute:str
  pos:int=0

  def __repr__(self) -> str:
    return f'<{self.name}, {self.pos}>'

@dataclass(init=True)
class TabelaSimbolos:
  table:List[Symbol] = field(default_factory=list)

  def insert(self, token:Token):
    symbol = Symbol((token.nome).value, token.atributo)
    if not symbol in self.table:
      symbol.pos = len(self.table) + 1
      self.table.append(symbol)
     # token.atributo = symbol.pos
      #print(f'Symbol {symbol} added to the table.')
    else:
      print(f'Simbolo {symbol} já existe.')
  
  def lookup(self, attribute:Union[str,int, float]) -> Union[Symbol, int]:
    if type(attribute) == str or type(attribute) == float:
      attribute = int(attribute)
    simbolo = self.table[attribute]
    if simbolo is not None:
      print(f'Simbolo {simbolo} encontrado.')
      return simbolo
    else:
      print(f'Não foi encontrado simbolo nessa posicao da tabela{attribute}')
      return -1

  def __repr__(self) -> str:
    msg = "Tabela de simbolos\n"
    for line, symbol in enumerate(self.table):
      msg += f'{line}: <{symbol.name}, {symbol.attribute}>\n'
    return msg
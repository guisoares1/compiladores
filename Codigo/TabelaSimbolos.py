from cgitb import lookup
from dataclasses import dataclass, field
from typing import List, Union
from Token import Token, TKS

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
    symbol = Symbol(TKS(token.name).name, TKS(token.attribute).name)
    if not symbol in self.table:
      symbol.pos = len(self.table) + 1
      self.table.append(symbol)
      token.attribute = symbol.pos
      #print(f'Symbol {symbol} added to the table.')
    else:
      print(f'Symbol {symbol} already in table.')

  #todo Separated methods to avoid inserting duplicates
  def setID():
    pass

  def setNum():
    pass
  #todo Separated methods to avoid inserting duplicates
  
  def lookup(self, attribute:Union[str,int, float]) -> Union[Symbol, int]:
    if type(attribute) == int or type(attribute) == float:
      attribute = str(attribute)

    for symbol in self.table:
      if symbol.attribute == attribute:
        print(f'Symbol {symbol} find at line {symbol.pos}')
        return symbol
    print(f'Found 0 symbols with name/attribute equals to {attribute}')
    return -1

  def __repr__(self) -> str:
    msg = "SYMBOL TABLE\n"
    for line, symbol in enumerate(self.table):
      msg += f'{line}: <{symbol.name}, {symbol.attribute}>\n'
    return msg
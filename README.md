# Description
This project aims to simulate the structures of a compiler by implementing lexical, semantic, and syntactic analysis.
The language description is inside the descricao folder.

# Project Structure
- lexico.py: Responsible for returning the next token from the code.
- AnalisadorSintatico.py: Responsible for performing code analysis and returning whether it is valid or not.
- token.py: Entity that stores the language structure.
- TabelaSimbolos.py: Responsible for constructing the symbol table.
- preditivo.xlsx: Table that guides the compiler on the language rules.
- producoes.xlsx: Table that guides the compiler on the production tree of a non-terminal.

  ![alt text](https://github.com/guisoares1/Imagens/blob/main/estrutura-compilador.png)
  
# How to Use
The project includes the exemplo.txt file, where the code to be analyzed is placed.

With the Codigo directory open, execute the following command:
```ps
python .\AnalisadorSintatico.py
```
# Tasks
- [X] Lexical Analysis
- [x] Syntactic Analysis 
- [x] Predictive Table
- [X] Production Table
- [ ] Semantic Analysis

  

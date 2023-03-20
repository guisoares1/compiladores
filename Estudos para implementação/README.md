
# Requisitos técnicos
## Gramática livre de contexto

Uma gramática livre de contexto (GLC) é uma gramática formal onde todas as regras de produções são da forma A → α1. Em teoria de linguagens formais, uma linguagem livre de contexto (LLC) é uma linguagem gerada por alguma GLC2.

---
Aqui está um exemplo de uma gramática livre de contexto que gera a linguagem de todas as cadeias de “a” e “b” com o mesmo número de “a” e “b”:

**S → aSbS | bSaS | ε**

Neste exemplo, S é o símbolo inicial (não-terminal) e a e b são os símbolos terminais. A regra S → aSbS significa que podemos substituir o símbolo S por aSbS. A regra S → ε significa que podemos substituir o símbolo S por uma cadeia vazia (ε).
--
## Tokens
Tokens são os símbolos terminais em uma gramática. Eles representam as unidades básicas de uma linguagem e são gerados pelas regras de produção da gramática.

---
Aqui está um exemplo detalhado de como os tokens são usados na análise sintática de uma expressão matemática simples:

Suponha que temos a seguinte gramática livre de contexto para expressões matemáticas:

    expr → expr + term | expr - term | term
    term → term * factor | term / factor | factor
    factor → ( expr ) | num
    num → 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9

Nesta gramática, os tokens são os símbolos terminais: `+`, `-`, `*`, `/`, `(`, `)`, e os números de `0` a `9`.

Agora suponha que queremos analisar a seguinte expressão: `2 + 3 * (4 - 1)`. Primeiro, dividimos a expressão em tokens: `2`, `+`, `3`, `*`, `(`, `4`, `-`, `1`, `)`.

Em seguida, usamos a gramática para construir uma árvore de análise sintática para a sequência de tokens. Começamos com o símbolo inicial da gramática (`expr`) como a raiz da árvore. Em seguida, aplicamos as regras de produção da gramática para expandir os nós não-terminais na árvore até que todos os nós sejam terminais (ou seja, tokens).

Aqui está uma possível árvore de análise sintática para a sequência de tokens acima:

        expr
         |
     expr + term
     /       \
    num       term * factor
    |         /       \
    2      num        (expr)
            |          |
            3        expr - term
                     /       \
                   num       num
                    |         |
                    4         1

Esta árvore mostra como a sequência de tokens pode ser derivada pelas regras da gramática. A partir desta árvore podemos determinar que a sequência de tokens é válida de acordo com as regras da linguagem.
--
## Expressões regulares 
Expressões regulares são padrões que descrevem conjuntos de cadeias de caracteres. Elas podem ser usadas para definir os padrões dos tokens em uma gramática.


---
Aqui está um exemplo mais simples de como as expressões regulares podem ser usadas para definir os padrões dos tokens em uma gramática:

Suponha que temos uma gramática simples para sentenças em inglês que inclui apenas palavras e espaços. Os tokens nesta gramática podem incluir palavras (como `ca`t ou `dog`) e espaços.

Podemos usar expressões regulares para definir os padrões desses tokens. Por exemplo:

O padrão para uma palavra pode ser definido pela expressão regular `[a-zA-Z]+`, que corresponde a uma ou mais ocorrências de uma letra maiúscula ou minúscula.

O padrão para um espaço pode ser definido pela expressão regular `\s`, que corresponde a um único caractere de espaço em branco (como um espaço, tabulação ou nova linha).

Essas expressões regulares podem ser usadas por um analisador léxico (lexer) para dividir uma cadeia de entrada em tokens. Por exemplo, se a entrada for a cadeia `"the cat sat on the mat"`, o lexer pode usar as expressões regulares acima para gerar a seguinte sequência de tokens: `the`, `<space>`, `cat`, `<space>`, `sat`, `<space>`, `on`, `<space>`, `the`, `<space>`, `mat`.

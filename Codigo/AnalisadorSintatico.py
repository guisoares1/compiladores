import pandas as pd
import numpy as np
from Token import TokenEnum
from lexico import Analyzer
import os

#Vetor de Producoes
df2 = pd.read_excel('producoes.xlsx')
vetor_producoes = np.asarray(df2)

#Tabela de Análise Preditiva
df1 = pd.read_excel('preditivo.xlsx')
tabela_preditiva = np.asarray(df1)

#Numero de Linhas e Colunas da Tabela de Análise Preditiva
numero_linhasTab = df1.shape[0]
numero_colunasTab = df1.shape[1]

#Numero de Linhas e Colunas do Vetor de Producoes
numero_linhasVet = df2.shape[0]
numero_colunasVet = df2.shape[1]


#************************** FUNÇÕES AUXILIARES ************************************

#Função para pegar a tupla(linhas,coluna) de determinado simbolo. Ex: pegaLinhaColunaNaoTerminal("S")
def pega_linha_coluna(simbolo):
    for i in range(0,numero_linhasTab):
        for j in range(0,numero_colunasTab):
            if tabela_preditiva[i][j] == simbolo:
                return i,j
    return None

#Função que retorna valores da tabela, dado um Não Terminal e um Terminal. Ex: pegaValorTabela("declaracao_das_variaveis","identificador")
def pegaValorTabela(NTerminal, Terminal):
    linhaNTerminal, colunaNTerminal = pega_linha_coluna(NTerminal)
    linhaTerminal, colunaTerminal = pega_linha_coluna(Terminal) #erro aqui, continuar amanha

    return tabela_preditiva[linhaNTerminal][colunaTerminal]

#Função que retorna a producao correta, dado um Não Terminal e um Terminal. Ex: pega_vetor_producoes("S","programa")
def pega_vetor_producoes(NTerminal, Terminal):
    linhaNTerminal, colunaNTerminal = pega_linha_coluna(NTerminal)
    linhaTerminal, colunaTerminal = pega_linha_coluna(Terminal)
    valor = tabela_preditiva[linhaNTerminal][colunaTerminal]
    producao = vetor_producoes[valor-1][1]

    return producao.split()




class Nodo:

    def __init__(self, dado=None, nodo_anterior=None):
        self.dado = dado
        self.anterior = nodo_anterior

    def __repr__(self):
        return '%s -> %s' % (self.dado, self.anterior)


class Pilha:

    def __init__(self):
        self.topo = None
        self.lista = []
        self.lista2 = []
        self.tamanho = 0

    def __repr__(self):
        return "[" + str(self.topo) + "]"

    def push(self, novo_dado):

        # Cria um novo nodo com o dado a ser armazenado.
        novo_nodo = Nodo(novo_dado)

        self.lista.append(novo_dado)

        # Faz com que o novo nodo seja o topo da pilha.
        novo_nodo.anterior = self.topo

        # Faz com que a cabeça da lista referencie o novo nodo.
        self.topo = novo_nodo

        # Adiciona 1 no tamanho da pilha
        self.tamanho = self.tamanho + 1

    def pop(self):

        assert self.topo, "Impossível remover valor de pilha vazia."

        self.topo = self.topo.anterior

        self.tamanho = self.tamanho - 1

        self.lista.pop()

    def pilha_vazia(self):
        if self.topo == None:
            return True
        else:
            return False

    def pega_topo(self):
        if self.pilha_vazia():
            return None
        else:
            return self.lista[len(self.lista)-1]

def algoritmo_analise_preditiva(path):
    #Lista de terminais, filtrado pelas strings
    terminal = {member.value for member in TokenEnum if isinstance(member.value, str)}
    print(terminal)

    #Inicializa Floresta, Pilha, empilha simbolo inicial "S"
    pilha = Pilha()
    pilha.push("S")

    #Chama proximo token pro lexico
    analyzer = Analyzer(path)
    token = analyzer.lex()
    #Atribui token.tipo à variavel proxToken
    proxToken = (token.nome).name 

    #Enquanto pilha não for vazia
    while pilha.pilha_vazia() == False:
        x = pilha.pega_topo()
        if x in terminal:
            if x == proxToken:
                pilha.pop()
                token = analyzer.lex()
                proxToken = (token.nome).name 
            else:
                print(f"ERRO! TOKEN \"{token.atributo}\" NÃO ERA ESPERADO!\nErro presente na Linha: {token.linha} Coluna: {token.coluna} ".format(token.atributo))
                exit()
        else:
            valor = pegaValorTabela(x, proxToken)
            if valor == -1:
                print(f"ERRO! TOKEN \"{token.atributo}\" NÃO ERA ESPERADO!\nErro presente na Linha: {token.linha} Coluna: {token.coluna} ".format(token.atributo))
                exit()
            else:

                #Pega vetor de producao correspondente
                producao = pega_vetor_producoes(x, proxToken)

                #Retira o topo da pilha
                pilha.pop()
                #Pega vetor de producao correspondente
                producao = pega_vetor_producoes(x, proxToken)
                #Empilha todos os simbolos na ordem inversa
                if producao[0] != 'ε':
                    for i in range (0, len(producao)):
                        pilha.push(producao[i])

    #Ao sair do while, se o proxToken não for "$", erro!
    if proxToken != "$":
        print(f"ERRO! TOKEN \"{token.atributo}\" NÃO ERA ESPERADO!\nErro presente na Linha: {token.linha} Coluna: {token.coluna} ".format(token.atributo))
        exit()

    #Se o proxToken for "$", sucesso!
    else:
        print("SUCESSO! SEU PROGRAMA FOI ACEITO PELO ANALISADOR SINTÁTICO!")




if __name__ == '__main__':

    caminho_arquivo = os.path.join(os.getcwd(), "exemplo.txt")
    algoritmo_analise_preditiva(caminho_arquivo)

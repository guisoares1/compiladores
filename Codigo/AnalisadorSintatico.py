import pandas as pd
import numpy as np
from Token import TokenEnum
from lexico import Analyzer
import os

#Vetor de Producoes
dataframe_producoes = pd.read_excel('producoes.xlsx')
vetor_producoes = np.asarray(dataframe_producoes)

#Tabela de Análise Preditiva
dataframe_preditivo = pd.read_excel('preditivo.xlsx')
tabela_preditiva = np.asarray(dataframe_preditivo)

def pega_colum_preditiva(simbolo):
    if simbolo in dataframe_preditivo.columns:
        return dataframe_preditivo.columns.get_loc(simbolo)

    return -1

def pega_linha_preditiva(simbolo):
    linha_encontrada = dataframe_preditivo[dataframe_preditivo['NT'].str.contains(simbolo)].index[0]
    # Verificando se o valor foi encontrado
    return linha_encontrada


def pegaValorTabela(NTerminal, Terminal):
    print(NTerminal, Terminal)
    linhaNTerminal = pega_linha_preditiva(NTerminal)
    print("aqui")
    colunaTerminal = pega_colum_preditiva(Terminal) #erro aqui, continuar amanha
    print(linhaNTerminal, colunaTerminal)
    print(tabela_preditiva[linhaNTerminal][colunaTerminal])
    return tabela_preditiva[linhaNTerminal][colunaTerminal] # retorna valor da tabela preditiva

def pega_vetor_producoes(NTerminal, Terminal):
    linhaNTerminal = pega_linha_preditiva(NTerminal)
    colunaTerminal = pega_colum_preditiva(Terminal)
    valor = tabela_preditiva[linhaNTerminal][colunaTerminal]
    # print(valor)
    producao = vetor_producoes[valor-1][1]
    # vetor ao contrario para empilhar corretamente
    producao_copia = producao.split()
    producao_reverse = producao_copia[::-1]
    return producao_reverse

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

    #Inicializa Floresta, Pilha, empilha simbolo inicial "S"
    pilha = Pilha()
    pilha.push("S")

    #Chama proximo token pro lexico
    analyzer = Analyzer(path)
    token = analyzer.lex()
    #Atribui token.tipo à variavel proxToken
    proxToken = (token.nome).value 

    #Enquanto pilha não for vazia
    while pilha.pilha_vazia() == False:
        x = pilha.pega_topo()
        print(pilha, x)
        if x in terminal:
            if x == proxToken:
                pilha.pop()
                token = analyzer.lex()
                proxToken = (token.nome).value 
            else:
                print(f"TOKEN \"{proxToken}\" NÃO ERA ESPERADO!\nErro presente na Linha: {token.linha} Coluna: {token.coluna} ".format(token.atributo))
                exit()
        else:
            valor = pegaValorTabela(x, proxToken)
            # print(x,proxToken, valor)
            if valor == -1:
                print(f"TOKEN \"{(token.nome).value}\" NÃO ERA ESPERADO!\nErro presente na Linha: {token.linha} Coluna: {token.coluna} ".format(token.atributo))
                exit()
            else:

                #Retira o topo da pilha
                pilha.pop()
                #Pega vetor de producao correspondente
                producao = pega_vetor_producoes(x, proxToken)
                #print(producao)
                #Empilha todos os simbolos na ordem inversa
                if producao[0] != 'ε':
                    for i in range (0, len(producao)):
                        pilha.push(producao[i])

    #Ao sair do while, se o proxToken não for "$", erro!
    if proxToken != "$":
        print(f"TOKEN \"{token.atributo}\" NÃO ERA ESPERADO!\nErro presente na Linha: {token.linha} Coluna: {token.coluna} ".format(token.atributo))
        exit()

    #Se o proxToken for "$", sucesso!
    else:
        print("SEU PROGRAMA FOI ACEITO PELO ANALISADOR SINTÁTICO!")




if __name__ == '__main__':

    caminho_arquivo = os.path.join(os.getcwd(), "exemplo.txt")
    algoritmo_analise_preditiva(caminho_arquivo)

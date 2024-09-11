# Impotando API do gurobi
import gurobipy as gp
from gurobipy import GRB

# Importando bibliotecas auxiliares
import sys
import pandas as pd
from datetime import datetime

from auxiliares.manipulacaoArquivo import investimentoDF, tabela_produtosDF, tabela_ingrediente_produtoDF
from auxiliares.manipulandoModelo import cria_variaveis, cria_restricoes, cria_funcao_objetivo

if __name__ == '__main__':

  # Manipulando arquivo passado como argumento
  nome_arquivo = sys.argv[1]
  arquivo_csv = pd.read_csv(nome_arquivo)

  investimento = investimentoDF(arquivo_csv)
  tabela_produtos = tabela_produtosDF(arquivo_csv)
  tabela_ingrediente_produto = tabela_ingrediente_produtoDF(arquivo_csv)

  # Criando modelo
  modelo = gp.Model("ModeloTeste")
  
  # Adicionando variaveis
  modelo, variaveis = cria_variaveis(tabela_produtos, modelo)

  # Adicionando restrições
  modelo = cria_restricoes(tabela_ingrediente_produto, modelo)

  # Funcao objetivo
  modelo = cria_funcao_objetivo(tabela_ingrediente_produto, modelo)

  # Otimizando o modelo
  modelo.optimize()

  # Exportando
  resultado = []
  for variavel in modelo.getVars():
    resultado.append(
        {
            'Variavel': variavel.VarName,
            'Valor':  variavel.X
        }
    )
  nome_arquivo_resultado = f'./resultados/resultado_{datetime.today().strftime("%d%m%Y_%H%M")}.csv'
  pd.DataFrame(resultado).to_csv(nome_arquivo_resultado, sep='\t', encoding='utf-8', index=False, header=True)

# Funções auxiliares

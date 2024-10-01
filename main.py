# Impotando API do gurobi
import gurobipy as gp
from gurobipy import GRB

# Importando bibliotecas auxiliares
import sys
import pandas as pd
from datetime import datetime

from auxiliares.dados import Dados
from auxiliares.manipulandoModelo import cria_variaveis, cria_restricoes, cria_funcao_objetivo

if __name__ == '__main__':

  # Criando Tabelas de dados
  dados = Dados();

  # # Criando modelo
  # modelo = gp.Model("ModeloTeste")
  
  # # Adicionando variaveis
  # modelo, variaveis = cria_variaveis(tabela_produtos, modelo)

  # # Adicionando restrições 
  # modelo = cria_restricoes(tabela_ingrediente_produto, modelo, variaveis)

  # # Funcao objetivo
  # modelo = cria_funcao_objetivo(tabela_ingrediente_produto, modelo, variaveis)

  # # Otimizando o modelo
  # modelo.optimize()

  # # Exportando
  # resultado = []
  # for variavel in modelo.getVars():
  #   resultado.append(
  #       {
  #           'Variavel': variavel.VarName,
  #           'Valor':  variavel.X
  #       }
  #   )
  # nome_arquivo_resultado = f'./resultados/resultado_{datetime.today().strftime("%d%m%Y_%H%M")}.csv'
  # pd.DataFrame(resultado).to_csv(nome_arquivo_resultado, sep='\t', encoding='utf-8', index=False, header=True)
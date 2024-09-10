# Impotando API do gurobi
import gurobipy as gp
from gurobipy import GRB

# Importando bibliotecas auxiliares
import sys
import numpy as np
import pandas as pd

if __name__ == '__main__':

  # Lendo arquivo passado como argumento
  nome_arquivo = sys.argv[1]
  arquivo_csv = pd.read_csv(nome_arquivo)

  # Criando modelo
  modelo = gp.Model("ModeloTeste")
  
  # Adicionando variaveis
  produto_1 = modelo.addVar(vtype=GRB.INTEGER, name="produto_1")
  produto_2 = modelo.addVar(vtype=GRB.INTEGER, name="produto_2")

  # Adicionando restrições
  modelo.addConstr(produto_1 + produto_2 <= 20, "c0")

  # Funcao objetivo
  modelo.setObjective(produto_1 * 20 + produto_1 * 10, GRB.MAXIMIZE)

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
  pd.DataFrame(resultado).to_csv("resutado.csv", sep='\t', encoding='utf-8', index=False, header=True)


  
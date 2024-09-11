import pandas as pd
import gurobipy as gp
from gurobipy import GRB

def criaVariaveis(tabela_produtos: pd.DataFrame, modelo: gp.Model) -> tuple[gp.Model, list[gp.Var]]:
  variaveis = list[gp.Var]
  variaveis.append(modelo.addVar(vtype=GRB.INTEGER, name="produto"))

  return (modelo, variaveis)

def criaRestricoes(tabela_ingrediente_produto: pd.DataFrame, modelo: gp.Model) -> gp.Model:
  # modelo.addConstr(produto_1 + produto_2 <= 20, "c0")
  return modelo

def cria_funcao_objetivo(tabela_ingrediente_produto: pd.DataFrame, modelo: gp.Model) -> gp.Model:
  # modelo.setObjective(produto_1 * 20 + produto_1 * 10, GRB.MAXIMIZE)
  return modelo
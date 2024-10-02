# Impotando API do GLPK
import pulp

# Importando bibliotecas auxiliares
import sys
import pandas as pd
from datetime import datetime

from auxiliares.dados import Dados
from auxiliares.modeloGLPK import ModeloGLPK


if __name__ == '__main__':

  # Criando Tabelas de dados
  dados = Dados();

  # Criando modelo
  modelo = ModeloGLPK("Modelo_1", dados=dados, teste=False)

  vars = modelo.add_vars()
  modelo.add_constraints()
  modelo.add_objective_func()

  modelo.solve(pulp.GLPK())

  # Status da solução
  print(f"Status: {pulp.LpStatus[modelo.status]}")

  # Resultados
  print(f"Profit = {pulp.value(modelo.objective)}")

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
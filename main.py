# Impotando API do GLPK
import pulp

# Importando bibliotecas auxiliares
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
  status = pulp.LpStatus[modelo.status]
  resultado = pulp.value(modelo.objective)

  # Exportando
  resultadoX_it = []
  resultadoS_jt = []
  resultadoM_jt = []
  resultadoP_itt = []

  for variavel in vars["x_it"]:
    for var in variavel:
      resultadoX_it.append(
          {
              'Variavel': var,
              'Valor':  var.varValue
          }
      )

  for variavel in vars["s_jt"]:
    for var in variavel:
      resultadoS_jt.append(
          {
              'Variavel': var,
              'Valor':  var.varValue
          }
      )

  for variavel in vars["m_jt"]:
    for var in variavel:
      resultadoM_jt.append(
          {
              'Variavel': var,
              'Valor':  var.varValue
          }
      )

  for variavel in vars["pv_itt"]:
    for var in variavel:
      for v in var:
        resultadoP_itt.append(
            {
                'Variavel': v,
                'Valor':  v.varValue
            }
        )
        
  nome_arquivo_resultado = f'./resultados/resultado_{datetime.today().strftime("%d%m%Y_%H%M")}.txt'

  with open(nome_arquivo_resultado, 'w') as f:
    f.write(f"Status modelo: {status}\n")
    f.write(f"Resultado modelo: {resultado}\n")

    for dado in resultadoX_it:
      f.write(f'{dado["Variavel"]}: {dado["Valor"]}\n')

    for dado in resultadoS_jt:
      f.write(f'{dado["Variavel"]}: {dado["Valor"]}\n')

    for dado in resultadoM_jt:
      f.write(f'{dado["Variavel"]}: {dado["Valor"]}\n')

    for dado in resultadoP_itt:
      f.write(f'{dado["Variavel"]}: {dado["Valor"]}\n')
    
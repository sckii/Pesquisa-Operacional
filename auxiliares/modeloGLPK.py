import pandas as pd
import pulp
import numpy as np
from auxiliares.dados import Dados

class ModeloGLPK(pulp.LpProblem):
  _dados: Dados
  _variaveis: dict[str: pulp.LpVariable]
  _meseses: int = 12
  _Investimento = 300000
  _total_de_variaveis: int = 0
  _teste: bool = False

  def __init__(self, nome: str, dados: Dados, teste: bool = False) -> None:
    super().__init__(nome, pulp.LpMaximize)
    self._dados = dados
    self._teste = teste

  def add_vars(self) -> dict[str: pulp.LpVariable]:
    x_it = self.__varX_it()
    m_jt = self.__varM_jt()
    pv_itt = self.__varPV_itt()
    s_jt = self.__varS_jt()

    self._variaveis = {
      "x_it": x_it, 
      "m_jt": m_jt, 
      "pv_itt": pv_itt,
      "s_jt": s_jt
    }

    return self._variaveis

  def add_constraints(self) -> None:
    if self._teste:
      produtos = [self._dados.quantidade_prevista.index.values[0]]
    else:
      produtos = self._dados.quantidade_prevista.index.values
    
    rendimento = self._dados.rendimento.values
    quantidade_mes = self._dados.quantidade_prevista.values
    validade_produto = self._dados.validades.values.astype(float).astype(int)
    custo_compra_materia = self._dados.custo_compra_materia_prima
    rendimento_materia_prima = self._dados.rendimento_materia_prima
    quantidade_materia_produto = self._dados.quantidade_materia_produto
    
    # Demanda produto maxima
    for i in produtos:
      for t in range(self._meseses):
        demanda_produto = pulp.lpSum(
          self._variaveis["pv_itt"][i][n][t] for n in range(max(t - int(validade_produto[i][0]), 0), t)
        ) <= float(quantidade_mes[i][t])

        self += demanda_produto

    # Estoque produto >= 0
    for i in produtos:
      for t in range(self._meseses):
        estoque_produto = pulp.lpSum(
          self._variaveis["pv_itt"][i][t][n] for n in range(max(t - int(validade_produto[i][0]), 0), t)
        )

        self += (self._variaveis["x_it"][i][t] * float(rendimento[i][0])) - estoque_produto >= 0

    # Investimento máximo por mês
    for t in range(self._meseses):
      investimento_mensal = pulp.lpSum(
        self._variaveis["m_jt"][j][t] * float(custo_compra_materia.values[j][1]) for j in range(len(custo_compra_materia.values))
      ) 
      self += investimento_mensal >= 1000
      self += investimento_mensal <= self._Investimento

    # Estoque matéria prima
    for j in quantidade_materia_produto.columns.values:
      for t in range(self._meseses):
        estoque_materia_prima = pulp.lpSum(
          self._variaveis["x_it"][i][t] * float(quantidade_materia_produto.values[i][j]) for i in produtos
        ) 

        self += self._variaveis["s_jt"][j][t] >= 0
        if t - 1 < 0:
          self += (self._variaveis["m_jt"][j][t] * rendimento_materia_prima.values[j][0]) - estoque_materia_prima - self._variaveis["s_jt"][j][t] == 3000
        else:
          self += self._variaveis["s_jt"][j][t] + (self._variaveis["m_jt"][j][t] * rendimento_materia_prima.values[j][0]) - estoque_materia_prima - self._variaveis["s_jt"][j][t] == 3000
          
  def add_objective_func(self) -> None:
    if self._teste:
      produtos = [self._dados.quantidade_prevista.index.values[0]]
    else:
      produtos = self._dados.quantidade_prevista.index.values
    
    custo_compra_materia = self._dados.custo_compra_materia_prima
    preco_venda_produto = self._dados.preco_venda_produtos
    validade_produto = self._dados.validades.values.astype(float).astype(int)

    funcao_objetivo = pulp.lpSum(
      pulp.lpSum(
        pulp.lpSum(
          self._variaveis["pv_itt"][i][n][t] * preco_venda_produto.values[i][1] for n in range(max(t - int(validade_produto[i][0]), 0), t)
        ) for t in range(self._meseses)
      ) for i in range(len(produtos))
    )

    self += funcao_objetivo - pulp.lpSum(
      pulp.lpSum(
        self._variaveis["m_jt"][j][t] * float(custo_compra_materia.values[j][1]) for t in range(self._meseses)
      ) for j in range(len(custo_compra_materia.values))
    ) 

  # x_it : Quantidade de receitas do produto i produzidas no mês t.
  def __varX_it(self):
    if self._teste:
      produtos = [self._dados.quantidade_prevista.index.values[0]]
    else:
      produtos = self._dados.quantidade_prevista.index.values

    produto_mes = np.empty((len(produtos), self._meseses), dtype=object)

    for i in produtos:
      for t in range(self._meseses):
        produto_mes[i, t] = pulp.LpVariable(f"x_{i}.{t}", cat="Integer")

    self._total_de_variaveis += len(produto_mes)
    return produto_mes
  
  # m_it : Quantidade de materia prima j comprada no mês t.
  def __varM_jt(self):
    materia_primas = self._dados.rendimento_materia_prima.index.values
    
    materia_prima_mes = np.empty((len(materia_primas), self._meseses), dtype=object)

    for j in range(len(materia_primas)):
      for t in range(self._meseses):
        materia_prima_mes[j, t] = pulp.LpVariable(f"m_{j}.{t}", cat="Integer")

    self._total_de_variaveis += len(materia_prima_mes)
    return materia_prima_mes
  
  # pv_itt' :  Produto i produzido no mês t para vender no mês t'.
  def __varPV_itt(self):
    if self._teste:
      produtos = [self._dados.quantidade_prevista.index.values[0]]
    else:
      produtos = self._dados.quantidade_prevista.index.values
    
    produto_vendido = np.empty((len(produtos), self._meseses, self._meseses), dtype=object)

    for i in produtos:
      for t in range(self._meseses):
        for t_linha in range(self._meseses):
          produto_vendido[i, t, t_linha] = pulp.LpVariable(f"pv_{i}.{t}.{t_linha}", cat="Integer")

    self._total_de_variaveis += len(produto_vendido)
    return produto_vendido
  
  # s_it : Quantidade de materia prima j estocada no mes t.
  def __varS_jt(self):
    materia_primas = self._dados.rendimento_materia_prima.index.values
    
    materia_prima_mes = np.empty((len(materia_primas), self._meseses), dtype=object)

    for j in range(len(materia_primas)):
      for t in range(self._meseses):
        materia_prima_mes[j, t] = pulp.LpVariable(f"s_{j}.{t}", cat="Continuous")

    self._total_de_variaveis += len(materia_prima_mes)
    return materia_prima_mes
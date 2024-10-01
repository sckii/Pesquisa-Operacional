import pandas as pd
import gurobipy as gp
from gurobipy import GRB
from auxiliares.dados import Dados

class Modelo(gp.Model):
  _dados: Dados
  _variaveis: dict[str: gp.Var]
  _restricoes: dict[str: gp.Constr]
  _meseses: int = 13
  _Investimento = 10000

  _total_de_variaveis: int = 0

  def __init__(self, nome: str, dados: Dados) -> None:
    super().__init__(nome)

    self._dados = dados


  def add_vars(self) -> dict[str: gp.Var]:

    x_it = self.addVars(self.__varX_it(), vtype=GRB.CONTINUOUS)
    m_jt = self.addVars(self.__varM_jt(), vtype=GRB.CONTINUOUS)
    pv_itt = self.addVars(self.__varPV_itt(), vtype=GRB.INTEGER)

    self._variaveis = {
      "x_it": x_it, 
      "m_jt": m_jt, 
      "pv_itt": pv_itt
    }

    self.update()

    return self._variaveis

  def add_constraints(self) -> dict[str: gp.Constr]:
    produtos = self._dados.quantidade_prevista.index.values

    # Estoque >= 0
    quantidade_mes = self._dados.quantidade_prevista.values
    rendimento = self._dados.rendimento.values

    for i in produtos:
      for t in range(1, self._meseses + 1):
        total_produzido = self.__total_produzido_mes(self._variaveis["pv_itt"], i, t)
        self.addConstr((self._variaveis["x_it"] * rendimento[i][0]) - total_produzido >= 0)

    # Demanda maxima
    quantidade_mes = self._dados.quantidade_prevista.values

    for i in produtos:
      for t in range(1, self._meseses + 1):
        total_vendido = self.__total_vendido_mes(self._variaveis["pv_itt"], i, t)
        self.addConstr(total_vendido <= quantidade_mes[i][t])

    # Investimento máximo por mês
    custo_compra_materia = self._dados.custo_compra_materia_prima.values
    # for t in range(1, self._meseses + 1):
    #   [x for custo in custo_compra_materia: custo]


    return 0

  def cria_funcao_objetivo(tabela_ingrediente_produto: pd.DataFrame, modelo: gp.Model, variaveis: list[gp.Var]) -> gp.Model:
    # modelo.setObjective(produto_1 * 20 + produto_1 * 10, GRB.MAXIMIZE)
    return modelo
  
  # x_it : Quantidade de receitas do produto i produzidas no mês t.
  def __varX_it(self):
    produtos = self._dados.quantidade_prevista.index.values

    produto_mes: list[tuple] = []

    for i in produtos:
      for t in range(1, self._meseses):
        produto_mes.append((i, t))

    self._total_de_variaveis += len(produto_mes)
    return produto_mes
  
  # x_it : Quantidade de materia prima j comprada no mês t.
  def __varM_jt(self):
    materia_primas = self._dados.rendimento_materia_prima.index.values

    materia_prima_mes: list[tuple] = []

    for i in materia_primas:
      for t in range(1, self._meseses):
        materia_prima_mes.append((i, t))

    self._total_de_variaveis += len(materia_prima_mes)
    return materia_prima_mes
  
  # pv_itt' :  Produto i produzido no mês t para vender no mês t'.
  def __varPV_itt(self):
    produtos = self._dados.quantidade_prevista.index.values

    produto_vendido: list[tuple] = []

    for i in produtos:
      for t in range(1, self._meseses):
        for t_linha in range(1, self._meseses):
          produto_vendido.append((i, t, t_linha))

    self._total_de_variaveis += len(produto_vendido)
    return produto_vendido
  
  def __total_vendido_mes(self, pv_itt, i, t) -> list[float]:
    validade_produto = self._dados.validades.values
    total_vendido = 0

    for n in range(t, t - float(validade_produto[i][0])):
        total_vendido += pv_itt.get(i, n, t)
    
    return total_vendido

  def __total_produzido_mes(self, pv_itt, i, t) -> list[float]:
    validade_produto = self._dados.validades.values
    total_produzido = 0

    for n in range(t, t - float(validade_produto[i][0])):
        total_produzido += pv_itt.get(i, t, n)
    
    return total_produzido
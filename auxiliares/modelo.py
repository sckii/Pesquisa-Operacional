import pandas as pd
import gurobipy as gp
from gurobipy import GRB
from auxiliares.dados import Dados

class Modelo(gp.Model):
  _dados: Dados
  _variaveis: dict[str: gp.Var]
  _restricoes: dict[str: gp.Constr]
  _meseses: int = 12
  _Investimento = 10000
  _total_de_variaveis: int = 0
  _teste: bool = False

  def __init__(self, nome: str, dados: Dados, teste: bool = False) -> None:
    super().__init__(nome)
    self._dados = dados
    self._teste = teste

  def add_vars(self) -> dict[str: gp.Var]:
    x_it = self.addVars(self.__varX_it(), vtype=GRB.INTEGER)
    m_jt = self.addVars(self.__varM_jt(), vtype=GRB.INTEGER)
    pv_itt = self.addVars(self.__varPV_itt(), vtype=GRB.INTEGER)
    s_jt = self.addVars(self.__varS_jt(), vtype=GRB.INTEGER)

    self._variaveis = {
      "x_it": x_it, 
      "m_jt": m_jt, 
      "pv_itt": pv_itt,
      "s_jt": s_jt
    }
    self.update()

    return self._variaveis

  def add_constraints(self) -> None:
    if self._teste:
      produtos = [self._dados.quantidade_prevista.index.values[0]]
    else:
      produtos = self._dados.quantidade_prevista.index.values
    
    # Estoque produto >= 0
    quantidade_mes = self._dados.quantidade_prevista.values
    rendimento = self._dados.rendimento.values
    validade_produto = self._dados.validades.values.astype(float).astype(int)

    for i in produtos:
      for t in range(self._meseses):
        self.addConstr(
          (self._variaveis["x_it"].get((i, t)) * rendimento[i][0]) - 
          gp.quicksum(
            self._variaveis["pv_itt"].get((i,n,t)) for n in range(t, t - validade_produto[i][0])
          ) <= quantidade_mes[i][t], f"rE_{i}{t}")

    # Demanda produto maxima
    quantidade_mes = self._dados.quantidade_prevista.values

    for i in produtos:
      for t in range(self._meseses):
        self.addConstr(
          gp.quicksum(
            self._variaveis["pv_itt"].get((i,t,n)) for n in range(t, t - validade_produto[i][0])
          ) <= quantidade_mes[i][t], f"rD_{i}{t}")

    # Investimento máximo por mês
    custo_compra_materia = self._dados.custo_compra_materia_prima
    for t in range(self._meseses):
      self.addConstr(
        gp.quicksum(
          custo_compra_materia.values[j][1] * self._variaveis["m_jt"].get(j, t) for j in range(len(custo_compra_materia.index))
        ) <= (self._Investimento), f"rI_{i}{t}")
      
    # Estoque matéria prima
    materia_primas = self._dados.rendimento_materia_prima.index
    rendimento_materia_prima = self._dados.rendimento_materia_prima
    quantidade_materia_produto = self._dados.quantidade_materia_produto

    print(self._variaveis["s_jt"].get(0,0))

    for j in materia_primas:
      for t in range(self._meseses):
        if(t-1 < 0):
          self.add_constraints(
            self._variaveis["s_jt"].get(j,t) == self._variaveis["m_jt"].get(j,t) * rendimento_materia_prima[j] - gp.quicksum(
              self._variaveis["x_it"].get(i,t) * quantidade_materia_produto for i in range(len(produtos)))
          )
        else:
          self.add_constraints(
            self._variaveis["s_jt"].get(j,t) == self._variaveis["s_jt"].get(j,t-1) + self._variaveis["m_jt"] * rendimento_materia_prima[j] - gp.quicksum(
              self._variaveis["x_it"].get(i,t) * quantidade_materia_produto for i in range(len(produtos)))
          )

        self.add_constraints(
          self._variaveis["s_jt"].get(j,t) >= 0
        )
    
    self.update()

  def add_objective_func(tabela_ingrediente_produto: pd.DataFrame, modelo: gp.Model, variaveis: list[gp.Var]) -> gp.Model:
    # modelo.setObjective(produto_1 * 20 + produto_1 * 10, GRB.MAXIMIZE)
    return modelo
  
  # x_it : Quantidade de receitas do produto i produzidas no mês t.
  def __varX_it(self):
    if self._teste:
      produtos = [self._dados.quantidade_prevista.index.values[0]]
    else:
      produtos = self._dados.quantidade_prevista.index.values

    produto_mes: list[tuple] = []

    for i in produtos:
      for t in range(self._meseses):
        produto_mes.append((i, t))

    self._total_de_variaveis += len(produto_mes)
    return produto_mes
  
  # m_it : Quantidade de materia prima j comprada no mês t.
  def __varM_jt(self):
    materia_primas = self._dados.rendimento_materia_prima.index.values
    
    materia_prima_mes: list[tuple] = []

    for j in materia_primas:
      for t in range(self._meseses):
        materia_prima_mes.append((j, t))

    self._total_de_variaveis += len(materia_prima_mes)
    return materia_prima_mes
  
  # pv_itt' :  Produto i produzido no mês t para vender no mês t'.
  def __varPV_itt(self):
    if self._teste:
      produtos = [self._dados.quantidade_prevista.index.values[0]]
    else:
      produtos = self._dados.quantidade_prevista.index.values
    
    produto_vendido: list[tuple] = []

    for i in produtos:
      for t in range(self._meseses):
        for t_linha in range(self._meseses):
          produto_vendido.append((i, t, t_linha))

    self._total_de_variaveis += len(produto_vendido)
    return produto_vendido
  
    # s_it : Quantidade de materia prima j estocada no mes t.
  def __varS_jt(self):
    materia_primas = self._dados.rendimento_materia_prima.index.values
    
    materia_prima_mes: list[tuple] = []

    for j in materia_primas:
      for t in range(self._meseses):
        materia_prima_mes.append((j, t))

    self._total_de_variaveis += len(materia_prima_mes)
    return materia_prima_mes
  
  def __total_vendido_mes(self, pv_itt, i, t) -> list[float]:
    validade_produto = self._dados.validades.values.astype(float).astype(int)
    total_vendido = 0

    for n in range(t, t - validade_produto[i][0]):
        total_vendido += pv_itt.get(i, n, t)
    
    return total_vendido

  def __total_produzido_mes(self, pv_itt, i, t) -> list[float]:
    validade_produto = self._dados.validades.values.astype(float).astype(int)
    total_produzido = 0

    for n in range(t, t - validade_produto[i][0]):
        total_produzido += pv_itt.get(i, t, n)
    
    return total_produzido
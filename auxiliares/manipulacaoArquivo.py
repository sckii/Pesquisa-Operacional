import pandas as pd

def investimentoDF(arquivo_csv: pd.DataFrame) -> float:
  return float(arquivo_csv["investimento"][0])

def tabela_ingrediente_produtoDF(arquivo_csv: pd.DataFrame) -> pd.DataFrame:
  return arquivo_csv.drop(labels=["investimento"], axis=1),

def tabela_produtosDF(arquivo_csv: pd.DataFrame) -> pd.DataFrame:
  colunas = ["Ingrediente","Quantidade Líquida (utilizada na receita)","Valor Unitário","Rendimento","Quantidade Bruta","Valor Líquido","Valor Total"]
  return arquivo_csv.drop(labels=colunas, axis=1).drop_duplicates()
import pandas as pd

def investimentoDF(arquivo_csv: pd.DataFrame) -> float:
  return float(arquivo_csv["investimento"][0])

def tabela_ingrediente_produtoDF(arquivo_csv: pd.DataFrame) -> pd.DataFrame:
  return arquivo_csv.drop(labels=["investimento"], axis=1),

def tabela_produtosDF(arquivo_csv: pd.DataFrame) -> pd.DataFrame:
  return arquivo_csv.drop(labels=["ingrediente", "quantidade_ingrediente_produto", "custo_ingrediente", "investimento"], axis=1).drop_duplicates()
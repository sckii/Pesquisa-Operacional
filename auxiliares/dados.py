import pandas as pd
from os import listdir
from os.path import isfile, join

class Dados:
  def __init__(self) -> None:
    self.validades: pd.DataFrame = self.monta_validades_e_rendimento()[["validade"]]
    self.rendimento: pd.DataFrame = self.monta_validades_e_rendimento()[["rendimento"]]
    self.quantidade_materia_produto: pd.DataFrame = self.monta_quantidade_materiaprima_produto()
    self.quantidade_prevista: pd.DataFrame = self.monta_quantidade_prevista_e_preco().drop(columns=['Preco', 'produtos'])
    self.preco_venda_produtos: pd.DataFrame = self.monta_quantidade_prevista_e_preco()[["produtos","Preco"]]
    self.custo_compra_materia_prima: pd.DataFrame = self.monta_custo_compra_e_rendiment_matariaprima()[["Produto","Preço"]]
    self.rendimento_materia_prima: pd.DataFrame = self.monta_custo_compra_e_rendiment_matariaprima()[["quant"]]

  # Método para criar dados V_i (validade) e Rem_i (rendimento)
  def monta_validades_e_rendimento(self):
    nome_arquivos: list[str] = [f for f in listdir("./dados/fichas") if isfile(join("./dados/fichas/", f))]
    validades = pd.DataFrame()

    for nome_arquivo in nome_arquivos:
      arquivo_csv = pd.read_csv(f"./dados/fichas/{nome_arquivo}", sep=",", skiprows=4, nrows=8)

      novo_df = arquivo_csv.iloc[:, :3].drop(arquivo_csv.index[[4,5,6]], axis=0).fillna('').T.reset_index().drop("index", axis=1)

      df = pd.DataFrame()

      df["produto"] = [nome_arquivo.split(" ")[0]]
      df["rendimento"] = novo_df.iloc[2:3, 3:4].values[0].astype(str)
      df["validade"] = novo_df.iloc[1:2, 4:].values[0].astype(str)
      
      validades = pd.concat([validades, df])

    validades = validades.sort_values(by=["produto"], ascending=True)
    validades.set_index("produto", inplace=True, drop=True)
    return validades
  
  # Método para criar dados Rec_ij (quantidade de materia-prima j para o produto i)
  def monta_quantidade_materiaprima_produto(self):
    nome_arquivos: list[str] = [f for f in listdir("./dados/fichas/") if isfile(join("./dados/fichas/", f))]
    ingrediente_produto = pd.DataFrame()

    for nome_arquivo in nome_arquivos:
      arquivo_csv = pd.read_csv(f"./dados/fichas/{nome_arquivo}", sep=",", skiprows=13, nrows=15)

      novo_df = arquivo_csv.iloc[:, :1].dropna()
      novo_df["codigo "] = novo_df["codigo "].astype(int)
      novo_df_1 = arquivo_csv.iloc[:, 7:8].dropna().replace(',','.', regex=True).astype(float)
      novo_df[nome_arquivo.split(" ")[0]] = novo_df_1
      novo_df.set_index('codigo ', drop=True, inplace=True)

      novo_df.sort_index()
      
      ingrediente_produto = ingrediente_produto.merge(novo_df, left_index=True, right_index=True, how='outer')


    ingrediente_produto.sort_index().fillna(0, inplace=True)

    return ingrediente_produto.T.rename_axis("produto").astype(str).replace('nan','0', regex=True)

  # Método para criar dados Q_it (Quantidade prevista do produto i no mês t) e P_i (Preco de venda)
  def monta_quantidade_prevista_e_preco(self):
    arquivo_csv = pd.read_csv(f"./dados/Vendas 2023 - Estoque.csv", sep=",")

    novo_df = arquivo_csv
    novo_df["ID"] = (range(0, len(novo_df)))
    novo_df.set_index("ID", drop=True, inplace=True)
    
    return novo_df

  # Método para criar dados Q_it (Quantidade prevista do produto i no mês t) e P_i (Preco de venda)
  def monta_custo_compra_e_rendiment_matariaprima(self):
    arquivo_csv = pd.read_csv(f"./dados/MateriaPrima.csv", sep=",")

    novo_df = arquivo_csv
    novo_df.set_index('código', drop=True, inplace=True)
    novo_df = novo_df.drop(columns=["Frete", "unidade", "Rendimento %", "Custo und."])
    novo_df["Preço"] = novo_df["Preço"].replace(',','.', regex=True)

    return novo_df

# Trabalho 2 - DCC163 Pesquisa Operacional

> Trabalho de maximização de lucro para loja de produtos artezanais

## Perguntas feitas ao cliente

- Com que antecedência você decide o que será produzido?
  - Normalmente em uma ou duas semanas.

- Como você decide?
  - Definimos um estoque ideal para atender o volume de vendas mensal previsto. A produção é feita semanalmente, repondo as quantidades vendidas na semana anterior.

- A validade interfere na decisão da produção ou não é tão relevante?
  - Acaba não sendo tão relevante porque produzimos constantemente e quase que sob demanda. Nesse caso, dificilmente um produto fica em estoque por muito tempo.

- Com que antecedência faz os pedidos de matéria-prima?
  - A maioria dos pedidos são feitos mensalmente, alguns com intervalos maiores ou menores.
Precisamos equilibrar algumas variáveis como: prazo de entrega do fornecedor, a validade do insumo, a relação custo do frete por quantidade, preços melhores por quantidades maiores, etc

- Como decide o pedido?
  - De acordo com o volume de vendas/produção previsto para o mês seguinte.

## Modelagem
### Função Objetivo
$z=xi*Pi-mj*Cj-xi*Ci$

### Variáveis
$x_i$ : Quantidade do produto i produzido </br>
$m_i$ : Quantidade de matéria-prima j encomendada.

### Dados
$P_i$ : Preço de venda do produto i.</br>
$C_i$ : Custo de produção do produto i (sem a matéria-prima). </br>
$L_i$ : Quantidade de produto i na loja. </br>
$E_i$ : Quantidade do produto i encomendado. </br>
$Q_i$ : Quantidade mínima do produto i na loja. </br>
$R_{ij}$ : Quantidade da matéria-prima j para o produto i. </br>
$C_j$ : Custo de compra da matéria-prima j. </br>
$I$ : Investimento

### Restrições
Mínimo de produtos na loja: </br>
$\forall_i~|~L_i+x_i-E_i \geq Q_i$

Quantidade de matéria-prima necessária: </br>
$\forall_i~|~m_j \geq R_{ij} * x_i$

Investimento máximo: </br>
$\sum_i C_jm_j \leq I $

## Linguagem e Bibliotecas utilizadas
- Python3
- Gurobi Optimizer (gurobipy)
  - https://docs.gurobi.com/projects/optimizer/en/current/reference/python/model.html
- Numpy

## Criando ambiente virtual e execução
- Comando para criar ambiente virtual.
  ```cmd 
  python -m venv ./env 
  ```
- Comando para instalar dependencias.
  ```cmd 
  ./env/Script/python.exe -m pip install -r requirements.txt 
  ```
- Comando para execução do programa
  ```cmd 
  ./env/Scripts/python.exe main.py nomeArquivo.csv
  ```

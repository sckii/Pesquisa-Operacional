# Trabalho 2 - DCC163 Pesquisa Operacional

## Trabalho de maximização de lucro para uma loja de produtos artezanais

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
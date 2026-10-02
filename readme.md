# Análise Topológica de Geradores de Números Pseudoaleatórios (PRNGs)

Este repositório é dedicado ao estudo comparativo de **Geradores de Números Pseudoaleatórios (PRNGs)** utilizando técnicas de análise de dados e medidas topológicas para identificar estruturas geométricas ocultas e falhas de aleatoriedade em sequências numéricas.

---

## 📌 Visão Geral do Projeto

## 🔬 Geradores Analisados

### 1. Mersenne Twister (MT19937) — *Referência de Boa Qualidade*

O **Mersenne Twister (MT19937)** é um PRNG clássico, determinístico, com um período extremamente longo ($2^{19937}-1$) e excelentes propriedades estatísticas para uso geral.

No nosso experimento, ele atua como a referência de um gerador convencional de alta qualidade:

$$
\text{seed} \longrightarrow \text{MT19937} \longrightarrow x_1, x_2, \ldots, x_n
$$

Apesar de ser totalmente determinado pela semente inicial (*seed*), a sequência gerada distribui-se uniformemente no espaço multidimensional, servindo como linha de base para a avaliação topológica.

---

### 2. LCG / RANDU — *Referência Deliberadamente Problemática*

O **LCG (Linear Congruential Generator)** analisado utiliza a seguinte relação de recorrência:

$$
x_{n+1} = 65539 x_n \pmod{2^{31}}
$$

Estes parâmetros correspondem ao **RANDU**, um algoritmo amplamente utilizado na década de 1960 e famoso por suas falhas estruturais graves. 

Ao agrupar os pontos em tuplas tridimensionais:

$$
(x_t, x_{t+1}, x_{t+2})
$$

os pontos gerados não preenchem o espaço $3\text{D}$ de forma uniforme. Em vez disso, concentram-se em apenas **15 planos paralelos**, revelando uma forte dependência linear e uma estrutura geométrica altamente indesejada para simulações aleatórias.

---

## 🚀 Como Executar

## 📊 Resultados Esperados

## 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
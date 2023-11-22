# Projeto-integrador
Repositório para a disciplina de Projeto Integrador

## Introdução

Este projeto visa comparar algoritmos de análise de vidros em cenas de crime, utilizando um dataset obtido do repositório UCI. O dataset inclui informações sobre a composição química de diferentes tipos de vidros e suas classes correspondentes.

## Dataset UCI

O dataset foi retirado do repositório UCI e contém as seguintes colunas:

1. **Número de Identificação (ID):** 1 a 214
2. **RI (Índice de Refração):**
3. **Na (Sódio):** Percentagem em peso no óxido correspondente (atributos 4-10)
4. **Mg (Magnésio):**
5. **Al (Alumínio):**
6. **Si (Silício):**
7. **K (Potássio):**
8. **Ca (Cálcio):**
9. **Ba (Bário):**
10. **Fe (Ferro):**
11. **Tipo de Vidro (Classe):**
   - 0: Janelas do edifício (processadas)
   - 1: Janelas do edifício (não processadas)
   - 2: Janelas de veículo (processadas)
   - 3: Contentores
   - 4: Louça de mesa
   - 5: Faróis (nenhum nesta base de dados)

## Metodologia

1. **Coleta de Dados:**
   - Identificação de cenas de crime com vidros relevantes.
   - Coleta de amostras diversificadas de vidros.
   - Utilização do Repositório UCI para dados adicionais.

2. **Preparação dos Dados:**
   - Limpeza e normalização dos dados.
   - Divisão do dataset em conjuntos de treinamento e teste.
   - Codificação das características químicas dos vidros.

3. **Seleção e Treinamento dos Algoritmos:**
   - Escolha de algoritmos relevantes.
   - Treinamento e ajuste dos algoritmos com validação cruzada.

4. **Análise da Composição Química:**
   - Aplicação dos algoritmos no conjunto de teste.
   - Comparação de resultados e avaliação de métricas de desempenho.

5. **Conclusões:**
   - Análise crítica dos resultados.
   - Identificação de padrões e inconsistências.
   - Sugestões para aprimoramentos e direções futuras.


**Referências:**

Link para baixar o dataset: https://archive.ics.uci.edu/dataset/42/glass+identification

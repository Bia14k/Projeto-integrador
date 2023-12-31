# -*- coding: utf-8 -*-
"""projeto_forense.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XE1pyOezHzD5f6WgO-aP4GpSjTtaDXhp

0: janelas_do_edifício_float_processed
1: janelas_do_edifício_não_float_processed
2: Janelas_de_veículo_float_processed
3: contentores
4: loiça de mesa
5: faróis
-: janelas_de_veículo_nao_float_processed (nenhum nesta base de dados)

Informações adicionais
1. Número de identificação: 1 a 214
2. RI: índice de refração
3. Na: Sódio (unidade de medida: percentagem em peso no óxido correspondente, tal como os atributos 4-10)
4. Mg: Magnésio
5. Al: Alumínio
6. Si: Silício
7. K: Potássio
8. Ca: Cálcio
9. Ba: Bário
10. Fe: Ferro
11. Tipo de vidro: (atributo de classe)
   - 0: janelas_do_edifício_float_processed
   - 1: janelas_do_edifício_não_float_processed
   - 2: Janelas_de_veículo_float_processed
   - 3: contentores
   - 4: louça de mesa
   - 5: faróis
   - -: janelas_de_veículo_nao_float_processed (nenhum nesta base de dados)





     https://archive.ics.uci.edu/dataset/42/glass+identification
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import correlation
from sklearn.decomposition import PCA
import xgboost as xgb
import numpy as np

"""# PRE-PROCESS"""

!ls drive/MyDrive/Projeto\ aplicado\ -\ EU/

data = pd.read_csv('/content/glass_modificado - glass.csv (1).csv')
#data = pd.read_csv('drive/MyDrive/Projeto aplicado - EU/glass.csv')
#data = pd.read_csv('/content/drive/MyDrive/Projeto aplicado - EU/glass.csv')
print(data)

matcorr = np.corrcoef(data.to_numpy()[:, 1:].transpose())

"""# Mapa de Calor da Matriz de Correlação"""

sns.heatmap(matcorr, vmin=-1, vmax=1, cmap='jet')
# xticklabel

"""# Preparação de Dados: Exclusão da Coluna Inicial"""

datatu = data.to_numpy()[:, 1:]
datatu

"""# Extração da Última Coluna da Matriz de Dados Transformados"""

datatu[:,-1]

"""# Índice da Primeira Ocorrência do Valor 2 na Última Coluna"""

list(datatu[:,-1]).index(2)

janelas_edificil = np.mean(datatu[0:70,:], axis=0)

janelas_edificil[1] / np.sum(janelas_edificil[1:9])

janelas_edificil[1] / np.sum(janelas_edificil)

data.mean()

data.var()

data

from matplotlib import pyplot as plt
data.plot(kind='scatter', x='RI', y='NA', s=32, alpha=.8)
plt.gca().spines[['top', 'right',]].set_visible(False)

from matplotlib import pyplot as plt
data['NA'].plot(kind='hist', bins=20, title='NA')
plt.gca().spines[['top', 'right',]].set_visible(False)

"""# A MÉDIA E VARIÂNCIA POR TIPO DE VIDRO"""

data.groupby('TIPO_VIDRO').agg(['mean', 'median', 'var'])

import pandas as pd
from scipy.stats import shapiro

def shapiro_test_on_columns(dataframe):
    shapiro_results = {}

    for column in dataframe.columns:
        _, p_value = shapiro(dataframe[column])
        shapiro_results[column] = p_value

    return shapiro_results


# Aplicando o teste de Shapiro em todas as colunas
resultados_shapiro = shapiro_test_on_columns(data)

# Exibindo os resultados
for column, p_value in resultados_shapiro.items():
    print(f'Teste de Shapiro para {column}: p-value = {p_value}')

data.columns

data.head(3)

"""Correlação

cálculo de distância entre grupos

# Boxplots Comparativos dos Elementos por Classe de Vidro
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Selecionar colunas relevantes (excluindo as duas primeiras e a última)
elementos = data.columns[2:-1]

# Boxplot comparativo por classe
plt.figure(figsize=(12, 6))
sns.set(style="whitegrid")
for elemento in elementos:
    sns.boxplot(x='TIPO_VIDRO', y=elemento, data=data, width=0.5, palette='Set3')
plt.title('Boxplot Comparativo por Classe')
plt.show()

"""# Boxplots Comparativos por Elemento e Classe de Vidro"""

# Boxplot comparativo por classe
#plt.figure(figsize=(9, 18))
fig, axes = plt.subplots(3, 2, figsize=(9, 18))
sns.set(style="whitegrid")
#elemento = elementos[1]
#sns.boxplot(x='TIPO_VIDRO', y=elemento, data=data, width=0.5, palette='Set3')
#for elemento in elementos:
for i in range(2):
  for j in range(3):
    elemento = elementos[i*3+j]
    sns.boxplot(ax=axes[j, i], x='TIPO_VIDRO', y=elemento, data=data,  palette='Set3')
plt.title('Boxplot Comparativo por Classe')
plt.show()

# Histogramas por atributo em subplots
fig, axes = plt.subplots(nrows=1, ncols=len(elementos), figsize=(15, 5))
for i, elemento in enumerate(elementos):
    sns.histplot(data[elemento], kde=True, ax=axes[i], color='skyblue')
    axes[i].set_title(f'Histograma - {elemento}')
    axes[i].set_xlabel(elemento)
    axes[i].set_ylabel('Frequência')
plt.tight_layout()
plt.show()

# -------------------------------------------------------------
# ------------------  Barplots  ------------------------------
# -------------------------------------------------------------
# Barplot plot a bar of vector, it is count data and make labels

# If label is not defined data is generated based values of array
# Else if label is defined they are changed automatically

def barplot(vet, labels='', color='#1f77b4', title='', reverse=True):
    import matplotlib.pyplot as plt
    import numpy as np

    listvet = list(set(vet))
    i = 0
    while(i < len(listvet)):
        if(isinstance(listvet[i], (float))):
            del listvet[i]
            break
        i += 1
#    if(isinstance(listvet[0], (float))):
#        keys = sorted(listvet[1:], reverse=reverse)
#    else:
#        keys = sorted(listvet, reverse=reverse)
    keys = sorted(listvet, reverse=reverse)
    counts = np.zeros([len(keys)])
    for key in keys:
        counts[keys.index(key)] = vet.count(key)

    if(labels!=''):
        temp = [];
        for key in keys:
            temp.append(labels[key]);
        keys = temp;

    plt.barh(np.arange(len(keys)), list(counts), color=color )
    plt.yticks(np.arange(len(keys)), keys)
    plt.title(title)
    plt.show()

    return [keys, counts];

# ----------------------------------------------------
# -----------------  Correlation matrix  -------------
# ----------------------------------------------------
def correlation_matrix(df, labels=[], title='', labelx = [], labely = [], save=False, size = 6, scalecolor='default'):
    '''
        correlation_matrix(df, labels=[], title='', labelx = [], labely = [], save=False, size = 6, scalecolor='default')

        Inputs:
        ----------------------------
        df : numpy.array
            enter with correlation matrix, you can get a this with:
            >> import numpy as np
            >> df = np.corrcoef(mat)
        labels : list
        title : string
        labelx : list
        labely : list
        save : boolean
        size : integer
        scalecolor : string

    '''
    from matplotlib import pyplot as plt
    from matplotlib import cm as cm
    import numpy as np
#    df = (df+1)/2;
#    df = (df - df.min())/(df.max() - df.min())

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    if(scalecolor=='default'):
        cmap = cm.get_cmap('jet', 50)
    elif(scalecolor=='gray'):
        cmap = cm.get_cmap('gray')
    else:
        cmap = cm.get_cmap(scalecolor);
#    cax = ax1.imshow(df.corr(), interpolation="nearest", cmap=cmap)
    cax = ax1.imshow(df, interpolation="nearest", cmap=cmap)
    cax.set_clim(-1,1)

    ax1.grid(True)
    plt.title(title);

    if(len(labels)>0):
        # labels=['Sex','Length','Diam','Height','Whole','Shucked','Viscera','Shell','Rings',]
        T = np.arange(len(labels))
        ax1.set_yticks(T);
        ax1.set_xticklabels(labels,fontsize=size);
        ax1.set_yticklabels(labels,fontsize=size);
    if(len(labelx)>0):
        T = np.arange(len(labelx))
        ax1.set_xticks(T);
        ax1.set_xticklabels(labelx,fontsize=size);
    if(len(labely)>0):
        T = np.arange(len(labely))
        ax1.set_yticks(T);
        ax1.set_yticklabels(labely,fontsize=size)
    # Add colorbar, make sure to specify tick locations to match desired ticklabels
    tick = [];
    for i in range(0,11):
        tick.append(1-i*0.2)

#    for i in range(0,11):
#        tick.append(1-i*0.05)
#    fig.colorbar(cax, ticks=[.75,.8,.85,.90,.95,1])
#    fig.colorbar(cax, ticks=[.75,.8,.85,.90,.95,1])
    fig.colorbar(cax, ticks=tick)
#    fig.clim(-1, 1);

    plt.show()
    if(save):
        fig.savefig(title+'.png')

correlation_matrix(data, size=20)

"""fazer gráfico da normalidade



Histograma e boxplot

boxplot - comparativo por classe e outro (cada coluna com cada classe)
histograma por cada atributo(coluna)
criar subplots do matplotlib





distância de matrizes
falar em dos dados

análise dos boxplot

medidas de similaridade



"""

data_array = data.to_numpy()

# Calculando a Distância Euclidiana
euclidean_distances = pairwise_distances(data_array, metric='euclidean')

# Calculando a Correlação de Pearson
pearson_correlation = 1 - np.corrcoef(data_array)

# Exibindo os resultados
print("Distância Euclidiana:")
print(euclidean_distances)

print("\nCorrelação de Pearson:")
print(pearson_correlation)


mahalanobis_distances = []
for i in range(len(data_array)):
    mahalanobis_distance = np.sqrt((data_array[i] - mean_vector).T @ inv_cov_matrix @ (data_array[i] - mean_vector))
    mahalanobis_distances.append(mahalanobis_distance)

mahalanobis_distances = np.array(mahalanobis_distances)

print("\nDistância de Mahalanobis:")
print(mahalanobis_distances)

# Calculando a Distância de Mahalanobis
cov_matrix = np.cov(data_array, rowvar=False)
inv_cov_matrix = np.linalg.inv(cov_matrix)
mean_vector = np.mean(data_array, axis=0)

mahalanobis_distances = []
for i in range(len(data_array)):
    mahalanobis_distance = np.sqrt((data_array[i] - mean_vector).T @ inv_cov_matrix @ (data_array[i] - mean_vector))
    mahalanobis_distances.append(mahalanobis_distance)

mahalanobis_distances = np.array(mahalanobis_distances)


print("\nDistância de Mahalanobis:")
print(mahalanobis_distances)

"""# ANÁLISE DOS ALGORITMOS"""

# Dividindo os dados em características (X) e rótulos (y)
X = data.drop('TIPO_VIDRO', axis=1)
y = data['TIPO_VIDRO']

# Dividindo em treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalização
norm= Normalizer()
X_train = norm.fit_transform(X_train)
X_test = norm.transform(X_test)

# Regressão Logística
logistic_model = LogisticRegression()
logistic_model.fit(X_train, y_train)

# Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# XGBoost
xgb_model = xgb.XGBClassifier()
xgb_model.fit(X_train, y_train)

from sklearn.metrics import classification_report

# Regressão Logística
y_pred_logistic = logistic_model.predict(X_test)
print("Regressão Logística:")
print(classification_report(y_test, y_pred_logistic))

# Random Forest
y_pred_rf = rf_model.predict(X_test)
print("Random Forest:")
print(classification_report(y_test, y_pred_rf))

# XGBoost
y_pred_xgb = xgb_model.predict(X_test)
print("XGBoost:")
print(classification_report(y_test, y_pred_xgb))

import pandas as pd
import numpy as np
from matplotlib.pyplot as plt
from scipy import stats
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression

data = pd.read_csv('/content/glass_modificado - glass.csv (1).csv')

print(data.head())

print(data.dtypes)

print(data.isna().sum())

print(data.describe())

# 6. Teste de Normalidade de Shapiro-Wilk
for col in data.columns[1:9]:
    stat, p_value = stats.shapiro(data[col])
    print(f'O teste de Shapiro-Wilk para a variável {col} tem estatística = {stat} e p-valor = {p_value}')


# 8. Exploração de Relações entre Variáveis
correlation_matrix = data.corr()
print(correlation_matrix)



plt.figure(figsize=(12, 8))
sns.boxplot(data=data.drop(['ID', 'TIPO_VIDRO'], axis=1))
plt.title('Identificação de Outliers')
plt.show()

# 10. Transformações de Dados (Opcional)
# Dependendo dos resultados da análise exploratória, pode ser necessário realizar transformações nos dados.

# 11. Análise de Distribuição de Variáveis (Opcional)
# Considere a distribuição das variáveis para entender se elas seguem uma distribuição normal ou se têm algum padrão específico.

# 12. Análise de Grupos ou Clusters (Opcional)
# Se aplicável, tente identificar grupos naturais nos dados usando técnicas de clustering.

# 13. Documentação e Comunicação dos Resultados (Opcional)
# Mantenha um registro do processo de análise exploratória e, se necessário, prepare um relatório que comunique as principais descobertas.

# 14. Comparação de Algoritmos com K-Fold
# Vamos usar Random Forest, XGBoost e Regressão Linear

# Separando os dados em features (X) e target (y)
X = data.drop(['ID', 'TIPO_VIDRO'], axis=1)
y = data['TIPO_VIDRO']

# Definindo os modelos
models = {
    'Random Forest': RandomForestRegressor(),
    'XGBoost': XGBRegressor(),
    'Linear Regression': LinearRegression()
}

# Definindo o número de splits para K-Fold
kf = KFold(n_splits=5)

# Avaliando os modelos
for model_name, model in models.items():
    scores = []
    for train_index, test_index in kf.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)
        scores.append(score)

    print(f'{model_name}: Média do R^2 score = {np.mean(scores)}')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar seus dados para um DataFrame
df = pd.read_csv('seu_dataset.csv')

# 2.1. Estatísticas Descritivas

# Calcular média, mediana, desvio padrão e quartis
mean_composition = df['element_composition'].mean()
median_composition = df['element_composition'].median()
std_composition = df['element_composition'].std()
quartiles_composition = df['element_composition'].quantile([0.25, 0.5, 0.75])

mean_refraction = df['refraction_index'].mean()
median_refraction = df['refraction_index'].median()
std_refraction = df['refraction_index'].std()
quartiles_refraction = df['refraction_index'].quantile([0.25, 0.5, 0.75])

print("Estatísticas de Composição do Vidro:")
print(f"Média: {mean_composition}")
print(f"Mediana: {median_composition}")
print(f"Desvio Padrão: {std_composition}")
print("Quartis:")
print(quartiles_composition)

print("\nEstatísticas de Índice de Refração:")
print(f"Média: {mean_refraction}")
print(f"Mediana: {median_refraction}")
print(f"Desvio Padrão: {std_refraction}")
print("Quartis:")
print(quartiles_refraction)

# 2.2. Visualização de Dados

# Histograma
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
sns.histplot(df['element_composition'], kde=True)
plt.title('Histograma da Composição do Vidro')

plt.subplot(1, 2, 2)
sns.histplot(df['refraction_index'], kde=True)
plt.title('Histograma do Índice de Refração')
plt.tight_layout()
plt.show()

# Gráfico de Dispersão
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
sns.scatterplot(x='element_composition', y='refraction_index', data=df)
plt.title('Gráfico de Dispersão')

# Box Plot
plt.subplot(1, 2, 2)
sns.boxplot(x='element_composition', data=df)
plt.title('Box Plot da Composição do Vidro')
plt.tight_layout()
plt.show()
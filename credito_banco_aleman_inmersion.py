# -*- coding: utf-8 -*-
"""credito_banco_aleman_inmersion.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SNIZ4R88hs9bXMQyqfUQyhzE9SGfFksH

# INMERSIÓN DE DATOS CON PYTHON
"""

# prompt: Importa los siguientes módulos con sus respectivos alias: pandas, matplotlib, seaborn, , drive de google colab, warning

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.colab import drive
import warnings

drive.mount('/content/Drive')
warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)
global df_banco, resultados

df_banco = pd.read_csv('/content/Drive/MyDrive/german_credit.csv')
df_banco.head()

df_banco.shape

df_banco.columns

df_banco.info()

df_banco.account_check_status.value_counts().index

columnas = list(df_banco.select_dtypes(include='object').columns)
for columna in columnas:
  print(f'El nombre de la columna: {columna}')
  print(list(df_banco[f'{columna}'].value_counts().index))
  print('\n')

# dic = {'yes': 1, 'no': 0}
# df_banco['foreign_worker'] = df_banco['foreign_worker'].map(dic)
# df_banco['foreign_worker']
# df_banco.foreign_worker.value_counts()

def procesar_datos():
  global df_banco
  df_banco = df_banco.drop_duplicates() if df_banco.duplicated().any() else df_banco
  df_banco = df_banco.dropna() if df_banco.isnull().values.any() else df_banco

  a = {'no checking account': 4,
      '>= 200 DM / salary assignments for at least 1 year': 3,
      '0 <= ... < 200 DM': 2,
      '< 0 DM': 1
  }
  df_banco['account_check_status'] = df_banco['account_check_status'].map(a)

  a = { 'no credits taken/ all credits paid back duly' : 1,
      'all credits at this bank paid back duly' : 2,
      'existing credits paid back duly till now' : 3,
      'delay in paying off in the past' : 4,
      'critical account/ other credits existing (not at this bank)' : 5
  }
  df_banco['credit_history'] = df_banco['credit_history'].map(a)

  a = {'car (new)' : 1,
      'car (used)' : 2,
      'furniture/equipment' : 3,
      'radio/television' : 4,
      'domestic appliances' : 5,
      'repairs' : 6,
      'education' : 7,
      '(vacation - does not exist?)' : 8,
      'retraining' : 9,
      'business' : 10,
      'others' : 11
  }
  df_banco['purpose'] = df_banco['purpose'].map(a)

  a = {'unknown/ no savings account' : 1,
      '.. >= 1000 DM ' : 2,
      '500 <= ... < 1000 DM ' : 3,
      '100 <= ... < 500 DM' : 4,
      '... < 100 DM' : 5
  }
  df_banco['savings'] = df_banco['savings'].map(a)

  a = {'.. >= 7 years' : 1,
      '4 <= ... < 7 years' : 2,
      '1 <= ... < 4 years' : 3,
      '... < 1 year ' : 4,
      'unemployed' : 5
  }
  df_banco['present_emp_since'] = df_banco['present_emp_since'].map(a)

  a = {'male : divorced/separated' : 1,
      'female : divorced/separated/married' : 2,
      'male : single' : 3,
      'male : married/widowed' : 4,
      'female : single' : 5
  }
  df_banco['personal_status_sex'] = df_banco['personal_status_sex'].map(a)

  a = {'none' : 1,
      'co-applicant' : 2,
      'guarantor' : 3
  }
  df_banco['other_debtors'] = df_banco['other_debtors'].map(a)

  a = {'real estate' : 1,
      'if not A121 : building society savings agreement/ life insurance' : 2,
      'if not A121/A122 : car or other, not in attribute 6' : 3,
      'unknown / no property' : 4
  }
  df_banco['property'] = df_banco['property'].map(a)

  a = {'bank' : 1,
      'stores' : 2,
      'none' : 3
  }
  df_banco['other_installment_plans'] = df_banco['other_installment_plans'].map(a)

  a = {'rent' : 1,
      'own' : 2,
      'for free' : 3
  }
  df_banco['housing'] = df_banco['housing'].map(a)

  a = {'unemployed/ unskilled - non-resident' : 1,
      'unskilled - resident' : 2,
      'skilled employee / official' : 3,
      'management/ self-employed/ highly qualified employee/ officer' : 4
  }
  df_banco['job'] = df_banco['job'].map(a)

  a = {'yes, registered under the customers name ' : 1,
      'none' : 0
  }
  df_banco['telephone'] = df_banco['telephone'].map(a)

  a = {'yes' : 1,
      'no' : 0
  }
  df_banco['foreign_worker'] = df_banco['foreign_worker'].map(a)

procesar_datos()
df_banco.sample(5)

variables_discretas = ['personal_status_sex', 'age',
                       'duration_in_month', 'credit_amount','default']
df_banco[variables_discretas].tail(3)

dic_sexo = {2:1,5:1,1:0,3:0,4:0}
df_banco['sexo'] = df_banco['personal_status_sex'].map(dic_sexo)
df_banco['sexo']

def feature_engineering():
  global df_banco
  dic_sexo = {2:1, 5:1, 1:0, 3:0, 4:0}
  dic_est_civil = {3:1, 5:1, 1:0, 2:0, 4:0}
  df_banco['sexo'] = df_banco['personal_status_sex'].map(dic_sexo)
  df_banco['estado_civil'] = df_banco['personal_status_sex'].map(dic_est_civil)
  df_banco['rango_edad'] = pd.cut(x = df_banco['age'],
                                  bins=[18, 30, 40, 50, 60, 70, 80],
                                  labels = [1, 2, 3, 4, 5, 6]).astype(int)
  df_banco['rango_plazos_credito']=pd.cut(x = df_banco['duration_in_month'],
                                            bins=[1, 12, 24, 36, 48, 60, 72],
                                            labels = [1, 2, 3, 4, 5, 6]).astype(int)
  df_banco['rango_valor_credito']=pd.cut(x = df_banco['credit_amount'],
                                           bins=[1, 1000, 2000, 3000, 4000,
                                                 5000, 6000, 7000, 8000, 9000,
                                                 10000, 11000, 12000, 13000,
                                                 14000, 15000, 16000, 17000,
                                                 18000, 19000, 20000],
                                           labels = [1, 2, 3, 4, 5, 6, 7, 8, 9,
                                                     10, 11, 12, 13, 14, 15, 16,
                                                     17, 18, 19, 20]).astype(int)
  df_banco = df_banco.drop(columns=['personal_status_sex','age',
                                    'duration_in_month','credit_amount'])

feature_engineering()
df_banco.head(5)

df_banco.describe()

# Configuración del estilo de Seaborn
sns.set(style="whitegrid")

# Crear la figura y los ejes
plt.figure(figsize=(5, 4))

# Generar el histograma usando Seaborn
sns.countplot(data=df_banco, x='sexo')

# Agregar títulos y etiquetas
plt.title("Distribución por Sexo", fontsize=16)
plt.xlabel("Sexo", fontsize=14)
plt.ylabel("Frecuencia", fontsize=14)

# Mostrar el gráfico
plt.show()

def analisis_exploratorio():
  global df_banco
  histogramas = ['sexo','estado_civil','rango_plazos_credito','rango_edad','default']
  lista_histogramas = list(enumerate(histogramas))
  plt.figure(figsize = (30,20))
  plt.title('Histogramas')
  for i in lista_histogramas:
    plt.subplot(3, 2, i[0]+1)
    sns.countplot(x = i[1], data = df_banco)
    plt.xlabel(i[1], fontsize=20)
    plt.ylabel('Total', fontsize=20)

analisis_exploratorio()



"""# Desafios
 1. Analizar los datos de las distribuciones e identificar si hay algun valor o registros que no se deben considerar para el modelo.
 2. Investiga que es y como crear un mapa de calor para analizar la correlación de las variables.
 3. Crear una conclusión para cada uno de los gráficos del histograma. Mirar los datos y extraer conclusiones, porque es una habilidad esencial.
"""

# Desafio 1
def feature_engineering_new():
  global df_banco
  dic_sexo = {2:1, 5:1, 1:0, 3:0, 4:0}
  dic_est_civil = {3:1, 5:1, 1:0, 2:0, 4:0}
  df_banco['sexo'] = df_banco['personal_status_sex'].map(dic_sexo)
  df_banco['estado_civil'] = df_banco['personal_status_sex'].map(dic_est_civil)
  df_banco['rango_edad'] = pd.cut(x = df_banco['age'],
                                  bins=[18, 30, 40, 65, 80],
                                  labels=[1, 2, 3, 4]).astype(int)
                                  #extendí cada rango
  df_banco['rango_plazos_credito']=pd.cut(x = df_banco['duration_in_month'],
                                            bins=[1, 12, 24, 36, 72],
                                            labels=[1, 2, 3, 4]).astype(int)
  df_banco['rango_valor_credito']=pd.cut(x = df_banco['credit_amount'],
                                           bins=[1, 1000, 2000, 3000, 4000,
                                                 5000, 6000, 7000, 8000, 9000,
                                                 10000, 11000, 12000, 13000,
                                                 14000, 15000, 16000, 17000,
                                                 18000, 19000, 20000],
                                           labels = [1, 2, 3, 4, 5, 6, 7, 8, 9,
                                                     10, 11, 12, 13, 14, 15, 16,
                                                     17, 18, 19, 20]).astype(int)
  df_banco = df_banco.drop(columns=['personal_status_sex','age',
                                    'duration_in_month','credit_amount'])

feature_engineering_new()
df_banco.head(5)

def analisis_exploratorio_new():
    global df_banco

    # Columnas para los histogramas
    histogramas = ['sexo', 'estado_civil', 'rango_plazos_credito', 'rango_edad', 'default']
    lista_histogramas = list(enumerate(histogramas))

    # Configurar estilo de fondo y contexto
    sns.set_style("dark")  # Opciones: "whitegrid", "darkgrid", "white", "dark", "ticks"
    plt.figure(figsize=(30, 20))
    plt.gcf().set_facecolor("black")  # Fondo del canvas

    # Colores específicos para los gráficos
    colores = ["#FF5733", "#33FF57", "#3357FF", "#F1C40F", "#9B59B6"]

    # Título general
    plt.suptitle('Histogramas', fontsize=48, color="white")

    for i in lista_histogramas:
        plt.subplot(3, 2, i[0] + 1)
        sns.countplot(x=i[1], data=df_banco, color=colores[i[0]])
        plt.xlabel(i[1], fontsize=24, color="white")
        plt.ylabel('Total', fontsize=24, color="white")
        plt.xticks(fontsize=22, color="white")
        plt.yticks(fontsize=22, color="white")

    # Ajustar diseño
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

analisis_exploratorio_new()

# Desafio 2
# Calcular la matriz de correlación
correlacion = df_banco.corr()

# Crear el mapa de calor de todas las variables
plt.figure(figsize=(20, 8))  # Tamaño del gráfico
sns.heatmap(correlacion, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Mapa de calor de correlación')
plt.show()

# Selecciono variables que creo más relevantes

variables_relevantes = [
    'rango_plazos_credito', 'rango_valor_credito', 'installment_as_income_perc',
    'account_check_status', 'credit_history', 'savings',
    'present_emp_since', 'property', 'rango_edad', 'present_res_since'
]
df_relevantes = df_banco[variables_relevantes]

correlacion = df_relevantes.corr()

# Configurar el tamaño del mapa
plt.figure(figsize=(10, 8))

# Crear el mapa de calor
sns.heatmap(correlacion, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)

# Título del gráfico
plt.title('Mapa de calor: Correlación entre variables relevantes', fontsize=16)

# Mostrar el gráfico
plt.show()

"""## Desafio 3

### Conclusión histogramas:

1- Sexo: Indica que el 40% de las personas registradas son hombres y el resto mujeres.

2- Estado civil: Indica que hay mayor porcentaje de personas solteras que casadas o divorciadas.

3- Plazos créditos: Indica que el mayor porcentaje de créditos otorgados es entre 12 y 24 meses y el menor entre 36 y 72 meses.

4- Rango de edad: Indica que el mayor porcentaje de clientes está entre los 18 y 30 años y que hay muy poco porcentaje de personas mayores a 65 años



"""


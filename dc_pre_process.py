import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler

print("--- Pre-processamento de bc04.csv ---")

bcArquivo = pd.read_csv('bc04.csv')
print("Arquivo 'bc04.csv' carregado")
print(f"Matriz inicial: {bcArquivo.shape}")

# DROP nas colunas irrelevantes
bcProcessado = bcArquivo.drop(columns=['inv-nodes', 'node-caps', 'irradiat'])
print("\nColunas 'inv-nodes', 'node-caps', 'irradiat' irrelevantes removidas")

# DROP nas colunas duplicadas e mantém apenas o mais recente (ultimo)
bcProcessado = bcProcessado.drop_duplicates(subset=['pacient'], keep='last')
print("Registros duplicados removidos, mantendo apenas o mais recente")

bcProcessado = bcProcessado.rename(columns={'pacient': 'codigo'})
print("Renomeou pacient para 'codigo'")

# Eliminacao de valores ausentes como 'erro' ou '?' identificados 
# dropna (NaN Not a Number), para remover esses valores. Uso de um array com 
# os  valores ausentes identificads
valoresInvalidos = ['?', 'erro']
bcProcessado.replace(valoresInvalidos, np.nan, inplace=True)
# depois de convertido em NaN, possui uma funcao para remover eles
bcProcessado.dropna(inplace=True)
print("Registros com valores ausentes ou ruidos removidos")

# Salvando o arquivo pre-processado
bcProcessado.to_csv('bc_preprocessed.csv', index=False)
print("\nArquivo 'bc_preprocessed.csv' gerado")
print(f"Tamanho final da matriz: {bcProcessado.shape}\n")
print(bcProcessado.head())

print("\n--- Pre-processamento de pc04.csv ---")

pcArquivo = pd.read_csv('pc04.csv')
print("Arquivo 'pc04.csv' carregado")

pcProcessado = pcArquivo.drop_duplicates(subset=['codigo'], keep='last')
print("\nRegistros duplicados removidos")

pcProcessado.replace(valoresInvalidos, np.nan, inplace=True)
pcProcessado.dropna(inplace=True)
print("Registros com valores ausentes ou ruidos removidos")

pcProcessado = pcProcessado[(pcProcessado['sexo'] != 'M') & (pcProcessado['sexo'] != 'J')]
pcProcessado.drop(columns=['sexo'], inplace=True)
print("Registros do sexo 'M' e coluna 'sexo' removidos")

# Garantir que as colunas de peso e altura sao numeros.

# Transforma em string e substitui a virgula por ponto pra facilitar na conversao depois
pcProcessado['peso'] = pcProcessado['peso'].astype(str).str.replace(',', '.', regex=False)
pcProcessado['altura'] = pcProcessado['altura'].astype(str).str.replace(',', '.', regex=False)

# Converte as colunas para o tipo numerico.
# errors='coerce' transforma valor que nao eh numero em NaN
pcProcessado['peso'] = pd.to_numeric(pcProcessado['peso'], errors='coerce')
pcProcessado['altura'] = pd.to_numeric(pcProcessado['altura'], errors='coerce')

# Remove linhas daquela condicao errors='coerce'
pcProcessado.dropna(subset=['peso', 'altura'], inplace=True)
print("'peso' e 'coluna' sao numeros")

# Calculo IMC
pcProcessado['IMC'] = pcProcessado['peso'] / ((pcProcessado['altura'] / 100) ** 2).round(2)
intervalos = [0, 18.5, 25.0, 30.0, 35.0, 40.0, np.inf]
categorias = ['A', 'N', 'P', '1', '2', '3']
# Transforma em intervalos de 0 a 18.5 por exemplo, o right=False representa que o
# intervalo eh fechado na esquerda e aberto na direita
pcProcessado['IMC_cat'] = pd.cut(pcProcessado['IMC'], bins=intervalos, labels=categorias, right=False)
print("IMC_cat criado")

mapConvenio = {'particular': 'P', 'sus': 'S', 'convenio': 'C'}
pcProcessado['convenio'] = pcProcessado['convenio'].map(mapConvenio)
print("Convenio padronizado")

pcProcessado.to_csv('pc_preprocessed.csv', index=False, float_format='%.2f')
print("\nArquivo 'pc_preprocessed.csv' gerado")

print(pcProcessado.shape[0])

print("\n--- Primeira Integralizacao (bcc_parcial.csv) ---")

bcFinal = pd.read_csv('bc_preprocessed.csv')
pcFinal = pd.read_csv('pc_preprocessed.csv')

print("\nInfo de bcFinal:")
bcFinal.info()
print("\nInfo de pcFinal:")
pcFinal.info()

# Adesao de tipagem igual entre os codigos das colunas
if 'codigo' in bcFinal.columns and 'codigo' in pcFinal.columns:
    bcFinal['codigo'] = bcFinal['codigo'].astype(str)
    pcFinal['codigo'] = pcFinal['codigo'].astype(str)
    print("\nColuna 'codigo' padronizada pra string")
else:
    print("\nERRO: Coluna nao encontrada")
    exit()

# integralizacao (juncao dos dados)
bccParcial = pd.merge(bcFinal, pcFinal, on='codigo', how='inner')
print("Arquivos integrados")

bccParcial.drop(columns=['codigo'], inplace=True)
print("Atributo 'codigo' removido")

bccParcial.to_csv('bcc_parcial.csv', index=False, sep=',', float_format='%.2f')
print("\nArquivo 'bcc_parcial.csv' gerado")
print(f"Formato: {bccParcial.shape}\n")
print(bccParcial.head())

print("\n--- Finalizacao e Transformacao Numerica (bcc_final.csv) ---")

bccFinal = pd.read_csv('bcc_parcial.csv')
print("Arquivo 'bcc_parcial.csv' carregado")

# DROP na coluna IMC, foi substituida por IMC_cat
bccFinal.drop(columns=['IMC'], inplace=True)
print("\n'IMC' removido")

# Funcao MinMaxScaler do python para transformar o peso padronizado entre 0 e 1
minMax = MinMaxScaler()
bccFinal['peso'] = minMax.fit_transform(bccFinal[['peso']])
print("Peso padronizado")

# Funcao StandardScaler para ter media 0 e desvio padrao 1 para fins
# de padronizacao
scalerStd = StandardScaler()
bccFinal['altura'] = scalerStd.fit_transform(bccFinal[['altura']])
print("Altura padronizada")

bccFinal.to_csv('bcc_final.csv', index=False, sep=',', float_format='%.2f')
print("\nArquivo final 'bcc_final.csv' gerado")
print(f"Matriz final: {bccFinal.shape}\n")
print(bccFinal.head())
print(bccFinal.shape[0])
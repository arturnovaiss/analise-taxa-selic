import os
import time
import json
from random import random
from datetime import datetime
import requests
import csv
from sys import argv
import pandas as pd
import seaborn as sns

URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/10?formato=json'

# Etapa de Extração de Dados
for _ in range(0, 10):
    data_e_hora = datetime.now()
    data = datetime.strftime(data_e_hora, '%Y/%m/%d')
    hora = datetime.strftime(data_e_hora, '%H:%M:%S')

    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("Erro de conexão. Verifique sua conexão com a internet.")
        selic = None
        continue  # Pula para a próxima iteração
    except requests.HTTPError:
        print("Dado não encontrado, continuando.")
        selic = None
    except Exception as exc:
        print("Erro, parando a execução.")
        raise exc
    else:
        dados = json.loads(response.text)
        selic = float(dados[0]['valor']) + (random() - 0.5)  # Seleciona o valor do primeiro dado para simulação

    if not os.path.exists('./taxa-selic.csv'):
        with open(file='./taxa-selic.csv', mode='w', encoding='utf8') as fp:
            fp.write('data,hora,taxa\n')

    with open(file='./taxa-selic.csv', mode='a', encoding='utf8') as fp:
        fp.write(f'{data},{hora},{selic}\n')

    time.sleep(2 + (random() - 0.5))

print("Dados extraídos com sucesso e salvos em 'taxa-selic.csv'.")

# Etapa de Visualização dos Dados
# Extraindo as colunas hora e taxa
df = pd.read_csv('./taxa-selic.csv')

# Salvando o gráfico
grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
_ = grafico.set_xticklabels(labels=df['hora'], rotation=90)

# Salva o gráfico com o nome fornecido pelo usuário como parâmetro de entrada
output_filename = argv[1] if len(argv) > 1 else "grafico"
grafico.get_figure().savefig(f"{output_filename}.png")
print(f"Gráfico salvo como '{output_filename}.png'.")

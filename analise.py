import os
import time
import json
from random import random
from datetime import datetime
import requests
import pandas as pd
import seaborn as sns
from sys import argv

# URL da API do Banco Central
URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json'

# Etapa de extração dos dados
for _ in range(0, 10):
    data_e_hora = datetime.now()
    data = datetime.strftime(data_e_hora, '%Y/%m/%d')
    hora = datetime.strftime(data_e_hora, '%H:%M:%S')

    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("Erro de conexão. Verifique sua conexão com a internet.")
        taxa = None
        continue
    except requests.HTTPError as exc:
        print("Dado não encontrado, continuando.")
        taxa = None
    except Exception as exc:
        print("Erro, parando a execução.")
        raise exc
    else:
        dados = json.loads(response.text)
        taxa = float(dados[-1]['valor'].replace(',', '.')) + (random() - 0.5)

    if not os.path.exists('./taxa-bcb.csv'):
        with open(file='./taxa-bcb.csv', mode='w', encoding='utf8') as fp:
            fp.write('data,hora,taxa\n')

    with open(file='./taxa-bcb.csv', mode='a', encoding='utf8') as fp:
        fp.write(f'{data},{hora},{taxa}\n')

    time.sleep(2 + (random() - 0.5))

print("Sucesso na extração")

# Etapa de visualização dos dados
df = pd.read_csv('./taxa-bcb.csv')
grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
_ = grafico.set_xticklabels(labels=df['hora'], rotation=90)
grafico.get_figure().savefig(f"{argv[1]}.png")

print("Gráfico salvo com sucesso")

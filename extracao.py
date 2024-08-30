import os
import time
import json
from random import random
from datetime import datetime
import requests

URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json'

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
        continue  # Pula para a próxima iteração
    except requests.HTTPError as exc:
        print("Dado não encontrado, continuando.")
        taxa = None
    except Exception as exc:
        print("Erro, parando a execução.")
        raise exc
    else:
        dados = json.loads(response.text)
        # Pega a última taxa disponível
        taxa = float(dados[-1]['valor'].replace(',', '.')) + (random() - 0.5)

    if not os.path.exists('./taxa-bcb.csv'):
        with open(file='./taxa-bcb.csv', mode='w', encoding='utf8') as fp:
            fp.write('data,hora,taxa\n')

    with open(file='./taxa-bcb.csv', mode='a', encoding='utf8') as fp:
        fp.write(f'{data},{hora},{taxa}\n')

    time.sleep(2 + (random() - 0.5))

print("Sucesso")

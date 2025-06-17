import requests
import pandas as pd
from datetime import datetime

# Configurações
TOKEN = 'INSERIR_SEU_TOKEN'
BASE_URL = 'https://api-service.fogocruzado.org.br/api/v2/occurrences'
HEADERS = {
    'Authorization': f'Bearer {TOKEN}'
}


# Função para buscar os incidentes de tiroteio no Rio de Janeiro
def fetch_incidents_rj(start_date, end_date):
    incidents = []
    page = 1

    while True:
        params = {
            'order': 'ASC',
            'page': page,
            'take': 500,
            'idState': 'b112ffbe-17b3-4ad0-8f2a-2038745d1d14',  # ID do estado do Rio de Janeiro
            'idCities': 'd1bf56cc-6d85-4e6a-a5f5-0ab3f4074be3',  # ID da cidade do Rio de Janeiro
            'startDate': start_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'finalDate': end_date.strftime('%Y-%m-%dT%H:%M:%S')
        }

        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f'Erro {response.status_code}:', response.text)
            break

        data = response.json()
        pageMeta = data.get('pageMeta', {})
        results = data.get('data', [])

        if not results:
            print('Nenhum incidente encontrado.')
            break

        incidents.extend(results)
        print(f'Página {page}. Total: {len(incidents)}')
        if not pageMeta.get('hasNextPage'):
            break
        page += 1
    return incidents


# Executa a função e salva os dados
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)
dados = fetch_incidents_rj(start_date, end_date)
df = pd.DataFrame(dados)
df.to_csv('tiroteios_RJ_2024.csv', index=False, encoding='utf-8-sig')

print(f'{len(df)} registros salvos em "tiroteios_RJ_2024.csv"')